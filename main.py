import json

import requests
from bs4 import BeautifulSoup

headers = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36"
}

car_spans_list = []
cars_catalogs_info = []
for i in range(1, 101):
    url = f"https://auto.drom.ru/all/page{i}/"
    req = requests.get(url, headers)
    src = req.text

    soup = BeautifulSoup(src, "lxml")

    cars_catalog = soup.find_all("a", class_="css-ck6dgx")

    try:
        for car_catalog in cars_catalog:
            car_name = car_catalog.find("div", class_="css-13ocj84").find("span").text
            car_spans = car_catalog.find("div", class_="css-1fe6w6s").find_all("span")
            car_price = car_catalog.find("span", class_="css-46itwz").find("span").text + "₽"
            car_location = car_catalog.find("span", class_="css-1488ad").text
            car_time = car_catalog.find("div", class_="css-1x4jcds").find("div").text

            for car_span in car_spans:
                car_spans_list.append(car_span.text[:-1])

            car_info = ", ".join(car_spans_list)
            car_spans_list = []

            cars_info = {
                "Название": car_name,
                "Описание": car_info,
                "Цена": car_price,
                "Город": car_location,
                "Время добавления на сайт": car_time
            }

            cars_catalogs_info.append(cars_info)

    except Exception:
        print("error")

print(cars_catalogs_info)

with open("cars_catalogs.json", "w", encoding='utf-8') as file:
        json.dump(cars_catalogs_info, file, indent=4, ensure_ascii=False)