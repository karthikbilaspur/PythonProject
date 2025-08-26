import os

def carve_jpeg(directory):
    jpeg_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'rb') as f:
                    data = f.read()
                    if data.startswith(b'\xff\xd8\xff') and data.endswith(b'\xff\xd9'):
                        jpeg_files.append(file_path)
                        print(f"Found JPEG file: {file_path}")
                    else:
                        # Check for embedded JPEG files
                        start_idx = data.find(b'\xff\xd8\xff')
                        while start_idx != -1:
                            end_idx = data.find(b'\xff\xd9', start_idx)
                            if end_idx != -1:
                                jpeg_data = data[start_idx:end_idx + 2]
                                carve_jpeg_file(jpeg_data, len(jpeg_files))
                                jpeg_files.append(f"carved_jpeg_{len(jpeg_files)}.jpg")
                            start_idx = data.find(b'\xff\xd8\xff', start_idx + 1)
            except Exception as e:
                print(f"Error processing file: {file_path} - {e}")
    return jpeg_files

def carve_jpeg_file(jpeg_data, index):
    with open(f"carved_jpeg_{index}.jpg", 'wb') as f:
        f.write(jpeg_data)
    print(f"Carved JPEG file: carved_jpeg_{index}.jpg")

if __name__ == "__main__":
    directory = input("Enter directory path: ")
    jpeg_files = carve_jpeg(directory)
    print(f"Found {len(jpeg_files)} JPEG files.")