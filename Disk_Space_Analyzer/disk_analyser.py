import os

def get_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def disk_space_analyzer(path):
    print(f"Analyzing disk space for {path}...")
    total_size = get_size(path)
    print(f"Total size: {total_size / (1024 * 1024):.2f} MB")

    # Get top 10 largest files
    largest_files = []
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            size = os.path.getsize(fp)
            largest_files.append((fp, size))
    largest_files.sort(key=lambda x: x[1], reverse=True)
    print("Top 10 largest files:")
    for file, size in largest_files[:10]:
        print(f"{file}: {size / (1024 * 1024):.2f} MB")

if __name__ == "__main__":
    path = input("Enter path to analyze: ")
    disk_space_analyzer(path)