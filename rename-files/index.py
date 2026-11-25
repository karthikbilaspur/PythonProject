import os
import re
import shutil
import importlib
import argparse
from datetime import datetime
from typing import Any

INVALID_CHARS = r'<>:"/\\|?*\x00-\x1f'
def sanitize(name: str) -> str:
    """Strip characters illegal in Windows/macOS/Linux filenames."""
    name = re.sub(f'[{re.escape(INVALID_CHARS)}]', '_', name).strip().strip('.')
    return name or "renamed"

def log(msg: str):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def get_translations(new_name: str, languages: list[str]) -> dict[str, str]:
    """Translate once per language, not once per file."""
    try:
        translator_module = importlib.import_module("googletrans")
    except ImportError:
        print("ERROR: googletrans not installed. Run: pip install googletrans==4.0.0-rc1")
        print("Falling back to no-translation mode.")
        return {}
    translator: Any = translator_module.Translator()
    out: dict[str, str] = {}
    for lang in languages:
        lang = lang.strip()
        if not lang:
            continue
        try:
            translated_text: str = str(translator.translate(new_name, dest=lang).text)
            out[lang] = sanitize(translated_text)
            log(f"Translated '{new_name}' -> [{lang}] '{out[lang]}'")
        except Exception as e:
            print(f"WARNING: translation to '{lang}' failed ({e}). Skipping that language.")
    return out

def rename_files(directory: str, old_name: str, new_name: str,
                 languages: list[str] | None = None,
                 mode: str = "rename", dry_run: bool = False, force: bool = False):
    """
    mode="rename": os.rename (move) | mode="copy": shutil.copy2 (keep original)
    languages=None/[]: single rename. Otherwise: one copy per language.
    """
    if not os.path.isdir(directory):
        raise ValueError(f"Directory not found: {directory}")
    if not old_name:
        raise ValueError("Old name must not be empty.")
    if not new_name:
        raise ValueError("New name must not be empty.")
    if old_name == new_name and not languages:
        print("Old and new names are identical - nothing to do.")
        return

    # Translate ONCE
    targets: list[tuple[str | None, str]] = []  # (lang, replacement)
    if languages:
        trans = get_translations(new_name, languages)
        if not trans:
            print("No translations succeeded - nothing renamed.")
            return
        targets = [(lang, text) for lang, text in trans.items()]
    else:
        targets = [(None, sanitize(new_name))]

    matched = [f for f in os.listdir(directory) if old_name in f]
    if not matched:
        print(f"No files containing '{old_name}' in {directory}")
        return

    for filename in sorted(matched):
        src = os.path.join(directory, filename)
        if not os.path.isfile(src):
            continue
        for lang, replacement in targets:
            new_filename = filename.replace(old_name, replacement)
            dst = os.path.join(directory, new_filename)
            if src == dst:
                continue
            if os.path.exists(dst) and not force:
                log(f"SKIP {filename} -> {new_filename} (already exists, use --force to overwrite)")
                continue
            label = f"[{lang}] " if lang else ""
            if dry_run:
                log(f"DRY-RUN {label}{filename} -> {new_filename} ({mode})")
                continue
            if mode == "copy":
                shutil.copy2(src, dst)
                log(f"Copied {label}{filename} -> {new_filename}")
            else:
                # For multi-language rename: first language renames, rest copy from renamed file
                # so we don't lose the source mid-loop. Simpler: always copy, then delete source once.
                shutil.copy2(src, dst)
                log(f"Renamed {label}{filename} -> {new_filename}")
        # If mode is rename, remove original after all language copies are made
        if mode == "rename" and not dry_run:
            # Only delete if at least one target was created and differs from source
            if any(os.path.join(directory, filename.replace(old_name, r)) != src for _, r in targets):
                os.remove(src)

def rename_files_without_translation(directory: str, old_name: str, new_name: str, **kwargs: Any) -> Any:
    return rename_files(directory, old_name, new_name, languages=None, **kwargs)

def interactive():
    print("File Renamer")
    print("1. Rename files with translation (one copy per language)")
    print("2. Rename files without translation")
    choice = input("Enter your choice: ").strip()
    directory = input("Enter the directory path: ").strip()
    old_name = input("Enter the old name (substring to replace): ").strip()
    new_name = input("Enter the new name: ").strip()
    dry = input("Dry-run first? (y/n): ").strip().lower() == "y"
    if choice == "1":
        langs = [l.strip() for l in input("Enter languages comma-separated (e.g. en, es, fr): ").split(",") if l.strip()]
        rename_files(directory, old_name, new_name, languages=langs, mode="copy", dry_run=dry)
        if dry and input("Apply for real? (y/n): ").strip().lower() == "y":
            rename_files(directory, old_name, new_name, languages=langs, mode="copy", dry_run=False)
    elif choice == "2":
        rename_files_without_translation(directory, old_name, new_name, dry_run=dry)
        if dry and input("Apply for real? (y/n): ").strip().lower() == "y":
            rename_files_without_translation(directory, old_name, new_name, dry_run=False)
    else:
        print("Invalid choice.")

def cli():
    p = argparse.ArgumentParser(description="File Renamer")
    p.add_argument("directory", nargs="?", help="Directory containing files")
    p.add_argument("--old", dest="old", help="Substring to replace")
    p.add_argument("--new", dest="new", help="Replacement text")
    p.add_argument("--langs", help="Comma-separated languages, e.g. es,fr (enables translation copy mode)")
    p.add_argument("--copy", action="store_true", help="Copy instead of rename")
    p.add_argument("--dry-run", action="store_true", help="Preview only")
    p.add_argument("--force", action="store_true", help="Overwrite existing targets")
    args = p.parse_args()
    if not args.directory:
        interactive()
        return
    langs = [l.strip() for l in args.langs.split(",")] if args.langs else None
    rename_files(args.directory, args.old, args.new, languages=langs,
                 mode="copy" if args.copy or langs else "rename",
                 dry_run=args.dry_run, force=args.force)

if __name__ == "__main__":
    cli()
