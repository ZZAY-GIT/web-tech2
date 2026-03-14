import sys
import os


def files_sort(directory):
    files = []
    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)
        if os.path.isfile(full_path):
            files.append(entry)
    sorted_files = sorted(files, key=lambda x: (os.path.splitext(x)[1], x))
    return sorted_files


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python3 files_sort.py <путь_к_директории>")
        sys.exit(1)
    
    directory = sys.argv[1]
    
    if not os.path.isdir(directory):
        print(f"Ошибка: '{directory}' не является директорией или не существует")
        sys.exit(1)
    
    sorted_files = files_sort(directory)
    for filename in sorted_files:
        print(filename)