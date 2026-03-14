import sys
import os


def find_and_show_file(target_filename):
    start_dir = os.path.dirname(os.path.abspath(__file__))

    for root, dirs, files in os.walk(start_dir):
        if target_filename in files:
            full_path = os.path.join(root, target_filename)
            print(f"Найден файл: {full_path}\n")
            
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    for i, line in enumerate(f, 1):
                        if i > 5:
                            break
                        print(line.rstrip())
                return True
            except Exception as e:
                print(f"Ошибка при чтении файла: {e}")
                return True

    return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python file_search.py имя_файла")
        sys.exit(1)

    filename = sys.argv[1]

    if not find_and_show_file(filename):
        print(f"Файл {filename} не найден")