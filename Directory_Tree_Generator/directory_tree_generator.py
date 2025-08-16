import os
import argparse

def generate_directory_tree(directory: str, indent: int = 0, show_hidden: bool = False):
    try:
        files_and_dirs = os.listdir(directory)
        for item in files_and_dirs:
            if not show_hidden and item.startswith('.'):
                continue
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                print('  ' * indent + '+ ' + item + '/')
                generate_directory_tree(item_path, indent + 1, show_hidden)
            else:
                print('  ' * indent + '- ' + item)
    except PermissionError:
        print(f"Permission denied for directory: {directory}")
    except FileNotFoundError:
        print(f"Directory not found: {directory}")

def main():
    parser = argparse.ArgumentParser(description='Generate directory tree')
    parser.add_argument('directory', help='Path to the directory')
    parser.add_argument('-s', '--show-hidden', action='store_true', help='Show hidden files and directories')
    args = parser.parse_args()
    print(f"Directory Tree for {args.directory}:")
    generate_directory_tree(args.directory, show_hidden=args.show_hidden)

if __name__ == "__main__":
    main()