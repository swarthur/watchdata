import json
import urllib.request
import tomli

with open("../animedata/pyproject.toml", mode="rb") as pypr:
    ad_version = tomli.load(pypr)["project"]["version"]
print("AnimeData script version : ", ad_version)
dev_mode = False
ad_table = {
    "dev_branch": "dev-0.1/",
    "main_branch": "main/",
    "repository_url":
    "https://raw.githubusercontent.com/cassphir/ad_table/",
    "source_file_name": "animedata_source.json",
    "local_file_name": "animedata_local.json",
    "key_anime_name": "nom_anime",
    "key_seasons_episodes": "saisons_episodes",
    "key_episode_duration": "duree_episode",
    "key_episode_release_date": "date_sortie_episode",
    "key_episode_name": "nom_episode"}


def update_anime_lib():
    """Met à jour la librairie AnimeData depuis Github"""
    # STATUS : OK
    if dev_mode:
        urllib.request.urlretrieve(
            ad_table["repository_url"] +
            ad_table["dev_branch"] +
            ad_table["source_file_name"],
            ad_table["source_file_name"])
    else:
        urllib.request.urlretrieve(
            ad_table["repository_url"] +
            ad_table["main_branch"] +
            ad_table["source_file_name"],
            ad_table["source_file_name"])
    with open(ad_table["source_file_name"], encoding="utf-8") as ad_json:
        main_dict = json.load(ad_json)
        print("AnimeData library version :" +
              main_dict["ANIMEDATA-METADATA"]["animedata_version"],
              "#" +
              main_dict["ANIMEDATA-METADATA"]["lib_subversion"])
        print("Animes downloaded from Github :")
        for element in main_dict.values():
            if element["type"] == "anime":
                print(element[ad_table["key_anime_name"]])


def sauv_json(anime_dict):
    """Sauvegarde les données des animés contenues dans un dictionnaire dans un fichier JSON personalisé"""
    # STATUS : OK
    with open(ad_table["local_file_name"], "w", encoding="utf-8") as local_json:
        for anime in anime_dict.values():
            if anime["type"] != "anime":
                raise SyntaxError("dictionnary is not correctly formatted")
        json_dict = {
            "ANIMEDATA-METADATA": {
                "type": "metadata",
                "animedata_version": ad_version},
            **anime_dict}
        json.dump(obj=json_dict, fp=local_json, ensure_ascii=False)


def get_json_dict(ad_source=False):
    """Récupère le dictionnaire contenant les données depuis le fichier local d'AnimeData ou un fichier personalisé"""
    # STATUS : OK
    if ad_source:
        target_file = ad_table["source_file_name"]
    else:
        target_file = ad_table["local_file_name"]
    with open(target_file, "r", encoding="utf-8") as ad_json:
        anime_dict = json.load(ad_json)
    return anime_dict
