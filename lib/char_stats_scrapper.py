#importing required libraries
import pandas as pd
import requests
from time import sleep
from io import StringIO 
from bs4 import BeautifulSoup
import os
from pathlib import Path

#character name and element from genshin.csv from kaggle
genshin_character_data = pd.read_csv("dataset\genshin.csv", encoding='latin1')

#preprocessing genshin.csv
req_data = genshin_character_data[["character_name", "vision"]]
req_data = req_data.map(lambda x: x.lower())
req_data["character_name"] = req_data["character_name"].str.replace(" ", "-")
# print(req_data.head())


#scrapping character stats from keqingmains.com
def char_scrape(element, character):
    url = f"https://library.keqingmains.com/characters/{element}/{character}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    #Using BeautifulSoup to identify tables.
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table')

    # Use pd.read_html with the extracted table HTML
    if tables:
        html_content = str(tables)
        dfs = pd.read_html(StringIO(html_content))  # Wrap in StringIO
        print(len(dfs))
        return dfs
        

    else:
        print("No tables found on the page.")
        return 0
        




# iterate through all the characters 
for index, row in req_data.iterrows():
    print(row["character_name"]," : " ,end="")
    dfs = char_scrape(row["vision"], row["character_name"])

    directory_name = row["character_name"]
    directory_path = Path(f"character_tables/{directory_name}")

    try:
        directory_path.mkdir()
        print(f"Directory '{directory_path}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_path}' already exists.")
    finally:
        num = 1
        if dfs != 0 :
            for df in dfs:
                df.to_csv(f"{directory_path}/{str(num)}.csv", index=False)
                num +=1
