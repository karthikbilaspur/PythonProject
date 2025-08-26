import os
import shutil

def sort_files(directory):
    # Create folders for different file types
    folders = {
        'Documents': ['.txt', '.docx', '.pdf'],
        'Images': ['.jpg', '.png', '.gif'],
        'Videos': ['.mp4', '.avi', '.mov'],
        'Audio': ['.mp3', '.wav', '.ogg'],
        'Spreadsheets': ['.xls', '.xlsx', '.csv'],
        'Presentations': ['.ppt', '.pptx'],
        'Miscellaneous': []
    }

    for folder in folders:
        folder_path = os.path.join(directory, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    # Sort files into folders
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_extension = os.path.splitext(filename)[1].lower()
            for folder, extensions in folders.items():
                if file_extension in extensions:
                    shutil.move(file_path, os.path.join(directory, folder))
                    print(f"Moved {filename} to {folder}")
                    break
            else:
                shutil.move(file_path, os.path.join(directory, 'Miscellaneous'))
                print(f"Moved {filename} to Miscellaneous")

if __name__ == "__main__":
    directory = input("Enter directory path to sort: ")
    sort_files(directory)