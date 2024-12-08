### *Данный код - просто пример испоьзования данных библиотек**

#### *Пишите код, исходя из разметки сайта, который вы парсите**



## Веб-парсер для получения информации о товарах

Этот проект представляет собой Python-скрипт, который собирает информацию о товарах с веб-страницы [ryvok.ru](https://ryvok.ru/instrumenty/shlifmashiny/) и загружает данные в Google Таблицы.

## Требования

- Python 3.x
- Необходимые библиотеки:
  - `requests` (для отправки HTTP-запросов)
  - `beautifulsoup4` (для парсинга HTML)
  - `pandas` (для обработки данных)
  - `gspread` (для работы с Google Таблицами)

Установите зависимости с помощью:

```
pip install requests beautifulsoup4 pandas gspread
```
## Как это работает

Скрипт выполняет следующие шаги:

1. **Запросы к страницам**: Скрипт отправляет HTTP-запросы на сайт и получает HTML-контент с товарами.
2. **Парсинг HTML**: Извлекается информация о товарах, включая:
   - Название товара
   - Статус (если указан)
   - Цена (с удалением лишних символов и валютных знаков)
3. **Обработка пагинации**: Скрипт автоматически определяет количество страниц и собирает данные со всех страниц.
4. **Хранение данных**: Собранные данные сохраняются в pandas DataFrame.
5. **Загрузка в Google Таблицы**: Используется библиотека `gspread` для загрузки собранной информации в Google Таблицы.

## Код скрипта с коментариями 
```
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import gspread

data = []  # Список для хранения данных о товарах
page = 1  # Начальная страница
max_page = 1  # Максимальное количество страниц для парсинга

# Цикл по всем страницам
while page <= max_page:
    res = requests.get(f"https://ryvok.ru/instrumenty/shlifmashiny/?page={page}")
    soup = bs(res.text, "html.parser")

    # Извлечение данных о товаре
    elements = soup.find_all("div", class_="app-product-card__wrap")
    for e in elements:
        title_element = e.find("div", class_="app-product-card__title")
        status_element = e.find("div", class_="app-product-card__status_color-success app-product-card__status")
        price_element = e.find("div", class_="app-product-card__price")

        # Добавление извлеченных данных в список
        data.append({
            "title": title_element.text.strip() if title_element else "Без названия",
            "status": status_element.text.strip() if status_element else "Статус не указан",
            "price": price_element.text.strip().replace('\xa0', '').replace("₽", "") if price_element else "Цена не указана",
        })
    
    # Обработка пагинации и нахождение последней страницы
    pagination = soup.find("div", class_="ui-pagination__numbers")
    if pagination:
        pages = [p.text.strip() for p in pagination.find_all("div", class_="ui-pagination__number")]
        int_pages = [int(p) for p in pages if p.isdigit()]
        max_page = max(int_pages) if int_pages else 1
    
    page += 1

# Сохранение данных в DataFrame
df = pd.DataFrame(data)
print(df)


# Загрузка данных в Google Таблицу
gc = gspread.service_account(filename="creds.json")
wks = gc.open("web_parsing").sheet1
wks.update([df.columns.values.tolist()] + df.values.tolist())
```



