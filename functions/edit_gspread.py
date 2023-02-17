from dotenv import load_dotenv
from googletrans import Translator
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
import os
import streamlit as st


# --- SETTINGS --- #
load_dotenv(verbose=True, dotenv_path='.env')
JSON_FILE_PATH = os.environ.get("JSON_FILE_PATH")
SHEET_KEY = os.environ.get("SHEET_KEY")


def add_titles(worksheet, titles, last_row):
    worksheet = worksheet
    titles = titles
    cell_list = worksheet.range("A"+ str(last_row + 1) + ":A" + str(last_row + len(titles)))
    print(f"last_row: {last_row}, Cell_list: {len(cell_list)}, titles: {len(titles)}")
    for num, title in enumerate(titles):
        cell_list[num].value = title
    worksheet.update_cells(cell_list, value_input_option="USER_ENTERED")

def add_row(worksheet, values, row_num):
    values = values
    tr = Translator(service_urls=['translate.googleapis.com'])
    values[-2] = tr.translate(values[-2], dest="ja").text
    worksheet.insert_row(values, row_num)

def check_db(worksheet, values):
    title = values[1]
    judge = ""
    cells = worksheet.findall(title, in_column=2)
    print(cells)
    if cells == []:
        judge = "new"
        return judge, cells
    else:
        if set(values) == set(worksheet.row_values(cells[0].row)):
            judge = "stay"
            return judge, cells
        else:
            judge = "update"
            return judge, cells[0]

def edit_row(worksheet, values, row_num):
    values = values
    tr = Translator(service_urls=['translate.googleapis.com'])
    values[-2] = tr.translate(values[-2], dest="ja").text
    cell_list = worksheet.range("A"+ str(row_num) + ":J" + str(row_num))
    for num, value in enumerate(values):
        cell_list[num].value = value
    worksheet.update_cells(cell_list, value_input_option="USER_ENTERED")

def get_worksheet():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    # credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE_PATH, scope)
    gs = gspread.authorize(credentials)
    spreadsheet_key = SHEET_KEY
    wb = gs.open_by_key(spreadsheet_key)
    ws_titles = wb.worksheet("titles")
    ws_db = wb.worksheet("DB")
    return ws_titles, ws_db

def get_last_row(worksheet):
    worksheet = worksheet
    list_of_lists = worksheet.get_all_values()
    return len(list_of_lists)

def get_titles(worksheet):
    title_dict = worksheet.get_all_records()
    title_list = []
    for r in title_dict:
        title_list.append(r["title"])
    return set(title_list)