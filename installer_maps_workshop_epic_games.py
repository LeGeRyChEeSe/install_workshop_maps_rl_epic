import json
import os
import shutil
import colorama
from colorama import Fore, Style


def is_exists(path):
    if os.path.exists(path):
        return True
    else:
        return False


def count_files(dir):
    return len([1 for x in list(os.scandir(dir)) if x.is_file()])


def get_files_list(dir):
    files = {}
    for file in os.scandir(dir):
        files[file.name] = file.path

    return files


def read(file: str = "maps.json"):
    if not is_exists(file):
        maps = {
            "backup": False,
            "language": "en_US",
            "rl_path": None,
            "original_maps": {
                "Labs_CirclePillars_P.upk": None,
                "Labs_Cosmic_V4_P.upk": None,
                "Labs_DoubleGoal_V2_P.upk": None,
                "Labs_Octagon_02_P.upk": None,
                "Labs_Underpass_P.upk": None,
                "Labs_Utopia_P.upk": None
            },
            "work_maps": {},
            "modified_maps": {}
        }
        write(maps)

    with open(file, "r", encoding="utf-8") as maps:
        return json.load(maps)


def write(content, mode: str = "w", file: str = "maps.json"):
    with open(file, mode, encoding="utf-8") as maps:
        json.dump(content, maps, indent=4)


def set_language(maps: dict, language: str):
    new_language = ""
    while new_language not in languages.keys():
        new_language = input(
            "\n".join(languages.keys()) + "\n" + languages[language]["set_language"])
        os.system("cls")

    language = maps["language"] = new_language
    write(maps)
    print(Fore.RED + languages[language]["language_set"] + Style.RESET_ALL)
    os.system("pause")
    main()


def make_dirs():
    try:
        os.mkdir("original_maps")
        os.mkdir("work_maps")
        os.mkdir("modified_maps")
    except OSError as error:
        pass


def get_map():
    maps_file: dict = read()

    if maps_file:
        while not maps_file["rl_path"] or not is_exists(maps_file["rl_path"]):
            maps_file["rl_path"] = os.path.join(input(
                languages[maps_file["language"]]["get_map"]), "TAGame\CookedPCConsole")
            os.system("cls")
    write(maps_file)
    make_dirs()
    return maps_file


def backup_original_maps(maps: dict):
    rl_path: str = maps["rl_path"]
    original_maps: dict = maps["original_maps"]

    print(Fore.BLUE + languages[maps["language"]]
          ["backup_original_maps1"] + Style.RESET_ALL)

    for file_name in original_maps.keys():

        path_to_file = os.path.join(rl_path, file_name)

        if is_exists(path_to_file):
            new_path = shutil.copy(path_to_file, "original_maps")
            original_maps[file_name] = new_path

    for _, values in languages.items():
        try:
            os.remove(
                f"original_maps\# ↓↓ {values['backup_original_maps2']} ! ↓↓")
        except:
            pass

    print(Fore.GREEN + languages[maps['language']]
          ['backup_original_maps2'] + Style.RESET_ALL)

    try:
        with open(f"original_maps\# ↓↓ {languages[maps['language']]['backup_original_maps2']} ! ↓↓", "x"):
            pass
    except:
        pass

    maps["backup"] = True

    write(maps)
    print(languages[maps["language"]]["backup_original_maps3"])


def restore_original_maps(maps: dict):
    rl_path: str = maps["rl_path"]
    original_maps: dict = maps["original_maps"]

    print(Fore.BLUE + languages[maps["language"]]
          ["restore_original_maps1"] + Style.RESET_ALL)

    for name, file in original_maps.items():
        old_file = os.path.join(rl_path, name)
        try:
            os.remove(old_file)
        except:
            pass
        shutil.copy(file, rl_path)

    print(Fore.GREEN + languages[maps["language"]]
          ["restore_original_maps2"] + Style.RESET_ALL)


def load_work_maps(maps: dict):
    while count_files("work_maps") == 0 or count_files("work_maps") > 6:
        print(Fore.BLUE + languages[maps["language"]]
              ["load_work_maps"] + Style.RESET_ALL)
        input()
        os.system("cls")

    maps["work_maps"] = get_files_list("work_maps")
    write(maps)


def make_modified_maps(maps: dict):
    rl_path = maps["rl_path"]
    work_maps: dict = maps["work_maps"]
    original_maps: dict = maps["original_maps"]
    modified_maps: dict = maps["modified_maps"]
    modified_maps.clear()
    temp_map = list(original_maps.keys())
    i = 0

    print(Fore.BLUE + languages[maps["language"]]["make_modified_maps1"].replace(
        "{maps['rl_path']}", maps['rl_path']) + Style.RESET_ALL)

    for name, file in work_maps.items():
        new_path = shutil.copy(file, "modified_maps")
        new_file = os.path.join("modified_maps", temp_map[i])
        if new_path != new_file and is_exists(new_file):
            os.remove(new_file)
        os.rename(new_path, new_file)
        os.remove(os.path.join(rl_path, temp_map[i]))
        shutil.copy(new_file, rl_path)

        modified_maps[name] = new_path

        i += 1

    write(maps)

    print(Fore.GREEN + languages[maps["language"]]
          ["make_modified_maps2"] + Style.RESET_ALL)


languages: dict = read("languages.json")


def main():
    os.system("cls")
    maps = get_map()
    language = maps["language"]

    user_choice = ""

    while user_choice not in ["0", "1", "2", "3"]:
        user_choice = input(languages[maps["language"]]["main"])

    os.system("cls")

    if user_choice == "1":
        if not maps["backup"]:
            backup_original_maps(maps)
        load_work_maps(maps)
        make_modified_maps(maps)

    elif user_choice == "2":
        restore_original_maps(maps)

    elif user_choice == "3":
        set_language(maps, language)
        return

    elif user_choice == "0":
        exit()


main()
os.system("pause")
