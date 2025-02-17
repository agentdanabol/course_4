import hashlib
import os
import sys

# Размер блока для вычисления хеша крупных файлов
BLOCK_SIZE = 65536

# Функция для вычисления SHA256 хеша файла
def compute_sha256(file_name):
    print(file_name + "\n")
    hash_sha256 = hashlib.sha256()
    try:
        with open(file_name, "rb") as f:
            for chunk in iter(lambda: f.read(BLOCK_SIZE), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except Exception as e:
        print(f"Ошибка чтения файла {file_name}: {e}")
        return None

# Запись хешей файлов в файл
def write_hashes_to_file(directory, output_file):
    with open(output_file, "w") as f:
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            if os.path.isfile(file_path):
                file_hash = compute_sha256(file_path)
                if file_hash:
                    f.write(f"{file_name}: {file_hash}\n")

# Загрузка хешей из файла в словарь
def load_hashes_from_file(file_path):
    hashes = {}
    try:
        with open(file_path, "r") as f:
            for line in f:
                name, hash_value = line.strip().split(": ")
                hashes[name] = hash_value
    except Exception as e:
        print(f"Ошибка загрузки хешей из {file_path}: {e}")
    return hashes

# Загрузка хешей из файла в словарь
def load_virus_hashes(file_path):
    try:
        with open(file_path, "r") as f:
            return f.read().lower()
    except Exception as e:
        print(f"Ошибка загрузки хешей вирусов из {file_path}: {e}")

# Сравнение текущих хешей с заданным списком и генерация отчета
def compare_hashes(directory, original_hash_file, virus_hash_file, report_file):
    original_hashes = {k: v.lower() for k, v in load_hashes_from_file(original_hash_file).items()}  
    virus_hashes = load_virus_hashes(virus_hash_file)
    print(virus_hashes)

    changed_files = {}
    infected_files = []

    with open(report_file, "w") as report:
        report.write("Origin hash:\n")
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            if os.path.isfile(file_path):
                current_hash = compute_sha256(file_path)
                report.write(f"{file_name}: {current_hash}\n")
                print("|"+ current_hash + "|\n")
                if file_name in original_hashes and original_hashes[file_name] != current_hash:
                    changed_files[file_name] = current_hash
                if current_hash in virus_hashes:
                    infected_files.append(file_name)

        report.write("\nChanged:\n")
        for file_name, file_hash in changed_files.items():
            report.write(f"{file_name}: {file_hash}\n")

        report.write("\nInfected:\n")
        for file_name in infected_files:
            report.write(f"{file_name}\n")

    # Удаление зараженных файлов
    for file_name in infected_files:
        try:
            os.remove(os.path.join(directory, file_name))
            print(f"Файл {file_name} удален.")
        except Exception as e:
            print(f"Ошибка удаления файла {file_name}: {e}")

# Основная программа
def main():
    current_dir = "infsec/lab5/Files"
    original_hash_file = "infsec/lab5/HashList.txt"
    virus_hash_file = "infsec/lab5/Files/VirusHashList.txt"
    report_file = "infsec/lab5/report.txt"

    # Генерация хешей файлов в текущей директории
    print("Вычисление исходных хешей файлов...")
    write_hashes_to_file(current_dir, original_hash_file)

    # Имитируем запуск программы, изменяющей файлы
    print("Запуск программы изменения файлов...")
    os.system("cd infsec/lab5/ && ./FC")

    # Сравнение хешей после изменения
    print("Сравнение хешей и поиск зараженных файлов...")
    compare_hashes(current_dir, original_hash_file, virus_hash_file, report_file)

    print(f"Проверка завершена. Отчет сохранен в {report_file}")

if __name__ == "__main__":
    main()
