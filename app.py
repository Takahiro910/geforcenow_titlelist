import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from streamlit_pills import pills
import functions.edit_gspread as egs


# --- Settings ---
ws_titles, ws_db = egs.get_worksheet()
st.set_page_config(layout="wide")

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False


#--- DataFrameをHTMLとして埋め込む準備 ---
html_template = """
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
  </head>
  <body>
    <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
    <div class="container">
        {table}
    </div>
  </body>
</html>
"""

st.title("GeForce NOW 対応タイトル一覧")

# --- DataFrameの準備 ---
df = pd.DataFrame(ws_db.get_all_values())
df.columns = list(df.loc[0, :])
df.drop(0, inplace=True)
df.reset_index(inplace=True)
df.drop('index', axis=1, inplace=True)


# --- 各Columnの加工 ---
df["img"] = df["img"].map(lambda s: "<img src='{}' width='500'>".format(s))
df["description"] = "<div style='width:800px;'>" + df["description"] + "</div>"
df["Title"] = "<a href='" + df["website"] + "'>" + df["title"] + "</a>"


# --- ジャンル選択 ---
df["genres"] = df["genres"].str.split(", ")
genres_li = df["genres"].values.tolist()
genres_set = set(genre for genres in genres_li for genre in genres)
genre_list = list(genres_set)
genre_list.remove("")
genre_list.append("All")
genre_list.sort()
select_genre = st.multiselect('探すジャンルを選択', genre_list, default='All')
if "All" in select_genre:
    select_genre = list(genres_set)
elif "" in select_genre:
    select_genre = list(genres_set)
df = df[df['genres'].apply(lambda x: bool(set(x) & set(select_genre)))]


# --- ソート機能 ---
sort_col = pills("ソートする列を選択", ["metacritic", "rating", "release_date"])
df = df.sort_values(by=sort_col, ascending=False)
df.reset_index(inplace=True, drop=True)


# --- オプション ---
include_nodata = st.checkbox("データが無い作品も含める")
if not include_nodata:
    df = df[df["release_date"] != "pass"]
    df = df[df["metacritic"] != "No data"]


# --- キーワード検索機能 ---
keyword_search = st.text_input(
    "キーワードで探す",
    label_visibility=st.session_state.visibility,
    disabled=st.session_state.disabled,
    placeholder="タイトルとか、点数とか、日付とか･･･！",
    )
if keyword_search:
    mask = df[df.apply(lambda x: x.str.contains(keyword_search, case=False, regex=True))]
    df = df[mask.any(axis=1)]


# --- ページ移動 ---
if 'page_num' not in st.session_state:
    st.session_state["page_num"] = 0
last_page = len(df)//30
prev, _ ,next = st.columns([1, 8, 1])

if next.button("次"):
    if st.session_state["page_num"] + 1 >= last_page:
        st.session_state["page_num"] = 0
    else:
        st.session_state["page_num"] += 1

if prev.button("前"):
    if st.session_state["page_num"] - 1 < 0:
        st.session_state["page_num"] = last_page-1
    else:
        st.session_state["page_num"] -= 1

_.write(f'現在のページ：{st.session_state["page_num"] + 1} (/{last_page})')

start_idx = st.session_state["page_num"] * 30
end_idx = (1 + st.session_state["page_num"]) * 30

df_table = df.reindex(columns=["Title", "img", "release_date", "metacritic", "rating", "genres", "description"]).iloc[start_idx:end_idx]


# --- DataFrameをHTMLのテーブルにして埋め込み ---
table = df_table.to_html(classes=["table", "table-bordered", "table-hover"], escape=False)
table = table.replace('<table border="1" class="dataframe table table-bordered table-hover">', '<table border="1" class="dataframe table table-bordered table-hover" width="1500">')
table = table.replace('<th>description</th>', '<th style="width:300px;">description</th>')
html_str = html_template.format(table=table)
components.html(html_str, height=800, scrolling=True)