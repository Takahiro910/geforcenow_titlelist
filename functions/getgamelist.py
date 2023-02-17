from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


# --- SETTINGS --- #
load_dotenv(verbose=True, dotenv_path='.env')
CHROMEDRIVER = os.environ.get("CHROMEDRIVER")
GFN_SITE = "https://www.nvidia.com/en-us/geforce-now/games/"


class GetGameList:

    # ---------- This is Using Selenium. ---------- #
    def __init__(self):
        self.driver = webdriver.Chrome(CHROMEDRIVER)

    def get_list(self):
        self.driver.get(GFN_SITE)
        time.sleep(5)
        game_titles = self.driver.find_elements(By.CLASS_NAME, "game-name")
        games = []
        for game in game_titles:
            title = game.text.rsplit(" (", 1)[0].replace(" - Epic Games Store", "").replace(" - Steam", "").replace("®", "").replace('"', '')
            if title in games:
                pass
            else:
                games.append(title)
        self.driver.close()
        print(f"取得したタイトル数：{len(games)}")
        # for game in games:
        #     with open(file, mode="a", encoding="utf-8", newline="") as f:
        #         writer = csv.writer(f)
        #         writer.writerow([game])
        return games