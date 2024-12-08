import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import gspread

data = []
page = 1
max_page = 1

while page <= max_page:

    res = requests.get(f"https://ryvok.ru/instrumenty/shlifmashiny/?page={page}")
    soup = bs(res.text, "html.parser")

    elements = soup.find_all("div", class_="app-product-card__wrap")

    for e in elements:
        title_element = e.find("div", class_="app-product-card__title")
        status_element = e.find("div", class_="app-product-card__status_color-success app-product-card__status")
        price_element = e.find("div", class_="app-product-card__price")

        data.append({
            "title": title_element.text.strip() if title_element else "Без названия",  
            "status": status_element.text.strip() if status_element else "Статус не указан",  
            "price": price_element.text.strip().replace('\xa0', '').replace("₽", "") if price_element else "Цена не указана",  
        })
    

    pagination = soup.find("div", class_="ui-pagination__numbers")
    if pagination:
        pages = [p.text.strip() for p in pagination.find_all("div", class_="ui-pagination__number")]
        
        int_pages = []
        for p in pages:
            if p.isdigit():
                int_pages.append(int(p))
        
        if int_pages:
            max_page = max(int_pages)
        else:
            max_page = 1

    page += 1
    df = pd.DataFrame(data)
    print(df)


    gc = gspread.service_account(filename="creds.json")
    wks = gc.open("web_parsing").sheet1
    wks.update([df.columns.values.tolist()] + df.values.tolist())



