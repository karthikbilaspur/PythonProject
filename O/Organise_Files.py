import os
from pathlib import Path

def get_input_path():
    while True:
        print_string = """
Type Path of the directory
OR
Press enter for running the script on current directory:
OR
Type quit
"""
        print(print_string + "\n\n")
        input_path = input("Input:")
        print("\n\n")

        if input_path.lower() == "quit":
            exit()
        elif input_path == "":
            return Path.cwd()
        else:
            path = Path(input_path)
            if path.exists() and path.is_dir():
                return path
            else:
                print("Invalid directory path. Please try again.")

def organize_files(directory):
    # Create a dictionary to store file extensions and their counts
    file_extensions = {}

    # Iterate over all files in the directory
    for file in directory.iterdir():
        if file.is_file():
            extension = file.suffix[1:]  # Get the file extension without the dot
            file_extensions[extension] = file_extensions.get(extension, 0) + 1

    # Print the count of files for each extension
    for extension, count in file_extensions.items():
        print(f"There are {count} files with extension {extension}")

    print("\n\n")

    # Create directories for each file extension and move files into them
    for extension in file_extensions:
        extension_dir = directory / extension
        extension_dir.mkdir(exist_ok=True)

        for file in directory.iterdir():
            if file.is_file() and file.suffix[1:] == extension:
                print(f"Moving {file.name} to {extension_dir.name}")
                file.rename(extension_dir / file.name)

def main():
    input_path = get_input_path()
    os.chdir(input_path)

    print(f"Organizing files in {input_path}...\n")
    organize_files(input_path)

    print("\nScript has organized files as per their extensions into different directories!\n")
    for item in input_path.iterdir():
        if item.is_dir():
            print(item.name)

if __name__ == "__main__":
    main()