import json
import os
import shutil


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
            "langages": ["fr_FR", "en_US"],
            "langage": "en_US",
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

    with open(file, "r") as maps:
        return json.load(maps)


def write(content, mode: str = "w", file: str = "maps.json"):
    with open(file, mode) as maps:
        json.dump(content, maps, indent=4)


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
                "Veuillez indiquer le chemin vers le dossier d'installation de Rocket League.\nPar exemple le chemin par défaut (si vous l'avez installé depuis Epic Games) est: 'C:\Program Files\Epic Games\\rocketleague'\n\nChemin = "), "TAGame\CookedPCConsole")
            os.system("cls")
    write(maps_file)
    make_dirs()
    return maps_file


def backup_original_maps(maps: dict):
    rl_path: str = maps["rl_path"]
    original_maps: dict = maps["original_maps"]

    print("Backup des fichiers originaux dans le dossier 'original_maps' en cours...")

    for file_name in original_maps.keys():

        path_to_file = os.path.join(rl_path, file_name)

        if is_exists(path_to_file):
            new_path = shutil.copy(path_to_file, "original_maps")
            original_maps[file_name] = new_path
    try:
        with open("original_maps\# ↓↓ NE PAS EFFACER CES FICHIERS ! ↓↓", "x"):
            pass
    except:
        pass

    write(maps)
    print("Backup des fichiers originaux réussie!")


def restore_original_maps(maps: dict):
    rl_path: str = maps["rl_path"]
    original_maps: dict = maps["original_maps"]

    print("Restauration des maps originales en cours...")

    for name, file in original_maps.items():
        old_file = os.path.join(rl_path, name)
        os.remove(old_file)
        shutil.copy(file, rl_path)

    print("Restauration des maps originales terminée!")


def load_work_maps(maps: dict):
    while count_files("work_maps") == 0 or count_files("work_maps") > 6:
        print("\nMerci de placer vos 6 maps workshop (6 maximum ou moins) dans le dossier 'work_maps' qui vient d'être créé (si vous lancez ce programme pour la première fois)\n\nAppuyez sur une touche pour lancer la copie des maps Workshops...")
        os.system("pause >nul")
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

    print(
        f"Copie des maps Workshops vers le dossier '{maps['rl_path']}', veuillez patienter un moment...")

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

    print("Opération terminée! Les maps Workshop ont bien été intégrées à Rocket League! Relancez le jeu pour en profiter ! :)\n\nPour remettre les maps par défaut relancez le programme et entrez '2'")


def main():
    maps = get_map()
    user_choice = ""

    while user_choice != "1" and user_choice != "2":
        user_choice = input(
            "1: Installer des maps Workshop\n2: Désinstaller les maps Workshop et remettre les maps originales\n\nVeuillez entre un numéro (1 ou 2): ")

    os.system("cls")

    if user_choice == "1":
        backup_original_maps(maps)
        load_work_maps(maps)
        make_modified_maps(maps)

    elif user_choice == "2":
        restore_original_maps(maps)


main()
os.system("pause")
