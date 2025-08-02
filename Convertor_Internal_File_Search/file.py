
import os

def search_files(directory, filename=None, extension=None, size=None):
    found_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            
            if (filename is None or filename.lower() in file.lower()) and \
               (extension is None or file.endswith(extension)) and \
               (size is None or file_size >= size[0] and file_size <= size[1]):
                found_files.append(file_path)
    
    return found_files

def main():
    directory = input("Enter the directory to search in: ")
    filename = input("Enter the filename to search for (leave blank for all files): ")
    extension = input("Enter the file extension to search for (leave blank for all extensions): ")
    size = input("Enter the file size range (e.g., 1000-10000, leave blank for all sizes): ")
    
    if size:
        size = tuple(map(int, size.split('-')))
    else:
        size = None
    
    if not filename:
        filename = None
    
    if not extension:
        extension = None
    else:
        extension = '.' + extension.lstrip('.')
    
    files = search_files(directory, filename, extension, size)
    
    if files:
        print(f"Found {len(files)} files:")
        for file in files:
            print(file)
    else:
        print("No files found.")

if __name__ == "__main__":
    main()