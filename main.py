import functions.edit_gspread as egs
from functions.getgamelist import GetGameList
from functions.getgameinfo import GetGameInfo
import time
from datetime import date


ws_titles, ws_db = egs.get_worksheet()
titles_last_row = egs.get_last_row(ws_titles)
db_last_row = egs.get_last_row(ws_db)

game_list = GetGameList()
games = game_list.get_list()
games = set(games)

recorded_titles = egs.get_titles(ws_titles)
new_titles = games - recorded_titles
print(new_titles)
egs.add_titles(ws_titles, new_titles, titles_last_row)
    
get_game_info = GetGameInfo()

for title in new_titles:
    print(title)
    id, release_date, genres, img = get_game_info.get_id(title)
    time.sleep(2)
    if id == "pass":
        website = "pass"
        metascore = "pass"
        rating = "pass"
        description = "pass"
    else:
        website, metascore, rating, description = get_game_info.get_game_info(id)
    add_date = str(date.today())
    
    values= [id, title, website, release_date, metascore, rating, genres, img, description, add_date]
    
    judge, cell = egs.check_db(ws_db, values)
    if judge == "new":
        cell = db_last_row + 1
        egs.add_row(ws_db, values, cell)
        db_last_row += 1
    elif judge == "update":
        egs.edit_row(ws_db, values, cell.row)
    else:
        pass
    
    time.sleep(2)