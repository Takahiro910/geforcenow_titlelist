from dotenv import load_dotenv
import os
import re
import requests
from bs4 import BeautifulSoup


# --- SETTINGS --- #
load_dotenv(verbose=True, dotenv_path='.env')
API_KEY = os.environ.get("API_KEY")
ENDPOINT = os.environ.get("ENDPOINT")


class GetGameInfo:

    def get_id(self, title):
        params = {
            "key": API_KEY,
            "search": title,
            "platforms": 4
        }
        res = requests.get(ENDPOINT, params=params)
        try:
            game = res.json()["results"][0]
        except:
            id = "pass"
            release_date = "pass"
            genres = "pass"
            img = "pass"
        else:
            id = game["id"]
            release_date = game["released"]
            if release_date == None:
                release_date = "0000-00-00"
            genres = ", ".join([genre["name"] for genre in game["genres"]])
            img = game["background_image"]
        # print(f"idとか: {id, release_date, metacritic, genres, img}")
        return id, release_date, genres, img

    def remove_tags(self, text):
        clean = re.compile("<.*?>")
        return re.sub(clean, "", text)

    def get_game_info(self, id):
        params = {
            "key": API_KEY,
        }
        res = requests.get(f"{ENDPOINT}/{id}", params=params)
        try:
            game_info = res.json()
        except:
            website = "No data"
            metascore = "No data"
            rating = "No data"
            description = "No data"
        else:
            # title = game_info["name"]
            website = game_info["website"]
            metascore = 0
            if game_info["metacritic_platforms"] != []:
                for platform in game_info["metacritic_platforms"]:
                    if platform["platform"]["platform"] == 4:
                        metascore = platform["metascore"]
            rating = game_info["rating"]
            description = game_info["description"]
            soup = BeautifulSoup(description, "html.parser")
            description = soup.text.replace('"', '”')
            description = self.remove_tags(description)
        return website, metascore, rating, description
