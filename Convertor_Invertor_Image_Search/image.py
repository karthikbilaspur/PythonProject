
import os
import argparse
from datetime import datetime

def search_photos(directory, extensions=None, recursive=True):
    try:
        if extensions is None:
            extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
        
        found_photos = []
        
        if recursive:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if os.path.splitext(file)[1].lower() in extensions:
                        found_photos.append(os.path.join(root, file))
        else:
            for file in os.listdir(directory):
                if os.path.isfile(os.path.join(directory, file)) and os.path.splitext(file)[1].lower() in extensions:
                    found_photos.append(os.path.join(directory, file))
        
        return found_photos
    except FileNotFoundError:
        print(f"Directory '{directory}' not found.")
        return []
    except PermissionError:
        print(f"Permission denied for directory '{directory}'.")
        return []

def filter_photos_by_date(photos, start_date=None, end_date=None):
    filtered_photos = []
    
    for photo in photos:
        try:
            timestamp = os.path.getmtime(photo)
            photo_date = datetime.fromtimestamp(timestamp)
            
            if (start_date is None or photo_date >= start_date) and (end_date is None or photo_date <= end_date):
                filtered_photos.append(photo)
        except OSError:
            print(f"Error accessing file '{photo}'.")
    
    return filtered_photos

def main():
    parser = argparse.ArgumentParser(description='Search for photos in a directory')
    parser.add_argument('directory', help='the directory to search in')
    parser.add_argument('-r', '--recursive', action='store_true', help='search recursively')
    parser.add_argument('-e', '--extensions', nargs='+', help='file extensions to search for')
    parser.add_argument('-s', '--start_date', help='start date for filtering (YYYY-MM-DD)')
    parser.add_argument('-d', '--end_date', help='end date for filtering (YYYY-MM-DD)')
    args = parser.parse_args()
    
    directory = args.directory
    recursive = args.recursive
    extensions = args.extensions
    
    try:
        start_date = datetime.strptime(args.start_date, '%Y-%m-%d') if args.start_date else None
        end_date = datetime.strptime(args.end_date, '%Y-%m-%d') if args.end_date else None
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return
    
    if extensions:
        extensions = [ext.lower() if ext.startswith('.') else '.' + ext.lower() for ext in extensions]
    
    photos = search_photos(directory, extensions, recursive)
    
    if start_date or end_date:
        photos = filter_photos_by_date(photos, start_date, end_date)
    
    if photos:
        print(f"Found {len(photos)} photos:")
        for photo in photos:
            print(photo)
    else:
        print("No photos found.")

if __name__ == "__main__":
    main()