import zipfile
import os
import io

# Глобальные переменные для хранения состояния
history = []  # История команд
current_dir = ""  # Текущая директория в эмуляторе

# Структура для пользователя в эмуляторе
class User:
    def __init__(self, name, uid, gid):
        self.name = name
        self.uid = uid
        self.gid = gid

# Карта пользователей
users = {
    "root": User("root", 0, 0),
    "user": User("user", 1000, 1000),
    "admin": User("admin", 1001, 1001)
}

# Открываем zip-архив как файловую систему
def open_zip(zip_path):
    try:
        return zipfile.ZipFile(zip_path, 'r')
    except zipfile.BadZipFile:
        print("Ошибка при открытии архива")
        return None

# Вывод списка файлов в текущей директории
def ls(zip_fs, path):
    print(f"Содержимое {path}:")
    for file_info in zip_fs.infolist():
        if file_info.filename.startswith(path) and file_info.filename != path:
            relative_path = file_info.filename[len(path):].strip('/')
            if '/' not in relative_path:
                print(relative_path)

# Переход в другую директорию
def cd(zip_fs, dir):
    global current_dir
    new_dir = os.path.join(current_dir, dir)
    if not any(f.filename.startswith(new_dir) for f in zip_fs.infolist()):
        print("Ошибка: директория не найдена")
    else:
        current_dir = new_dir + '/'

# Печать истории команд
def show_history():
    for i, cmd in enumerate(history):
        print(f"{i + 1}: {cmd}")

# Функция для изменения владельца файла
def chown(owner, file, zip_fs):
    usr = users.get(owner)
    if not usr:
        print(f"Ошибка: пользователь {owner} не найден")
        return

    file_path = os.path.join(current_dir, file)
    if not any(f.filename == file_path for f in zip_fs.infolist()):
        print(f"Ошибка: файл {file} не найден")
    else:
        print(f"Изменен владелец файла {file} на пользователя {usr.name} (UID: {usr.uid}, GID: {usr.gid})")

# Основной цикл командного интерфейса
def main():
    global current_dir
    user_name = "root"
    zip_path = "path/to/your/vfs.zip"  # Путь к архиву виртуальной файловой системы

    zip_fs = open_zip(zip_path)
    if not zip_fs:
        return

    current_dir = ""

    while True:
        command = input(f"{user_name}@emulator:{current_dir}$ ").strip()
        history.append(command)
        parts = command.split()
        if not parts:
            continue

        cmd, args = parts[0], parts[1:]

        if cmd == "ls":
            ls(zip_fs, current_dir)
        elif cmd == "cd":
            if args:
                cd(zip_fs, args[0])
            else:
                print("Укажите каталог")
        elif cmd == "history":
            show_history()
        elif cmd == "chown":
            if len(args) == 2:
                chown(args[0], args[1], zip_fs)
            else:
                print("Использование: chown <пользователь> <файл>")
        elif cmd == "exit":
            print("Выход из эмулятора")
            zip_fs.close()
            break
        else:
            print("Неизвестная команда:", cmd)

if __name__ == "__main__":
    main()
