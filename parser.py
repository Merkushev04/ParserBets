# -*- coding: utf-8 -*-
from telegram import send_message
import requests
from bs4 import BeautifulSoup
import json
import time

while 1 < 2:

    headers = { # что бы браузер не думал что мы бот
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
    }

    url = "https://www.footboom.com/betting/forecast"

    req = requests.get(url, headers=headers)
    src = req.text

    with open("index.html", "w") as file: # Записываем меню игр в файл
        file.write(src)

    with open("index.html") as file: # открываем меню игр
        src = file.read()

    soup = BeautifulSoup(src, "lxml") # указываем к чему применяем парсинг
    all_games = soup.find_all("a", class_="g-smooth_tr", limit=10) # указываем что ищем по елементу и классу

    games_hrefs = {}
    # games_links = set()

    count = 0
    for game in all_games: # перебираем ссылки и названия игр
        count += 1
        if count % 2 == 0: # ссылки идут парно, что бы убрать повторы
            game_name = game.text.strip()
            game_href = game.get("href")
            games_hrefs[game_name] = game_href # Делаем словарь для проверки повторов игр

            with open("games_dict.json", "w") as file:  # перезаписываю проверочный файл
                json.dump(games_hrefs, file, indent=4, ensure_ascii=False)

            with open("games_dict.json") as file: # открываем файл с записью прежних постов
                games_dict_file = file.read()

                if game_href in games_dict_file: # проверяем есть ли ссылка на эту страницу
                    print('Новых записей нет...')
                    break
                else:
                    print("Вижу новую игру, ворую данные...")

                    for name, link in games_hrefs.items():  # парсер данных со страницы матча
                        req = requests.get(link, headers=headers)
                        game_page = req.text

                        soup = BeautifulSoup(game_page, "lxml")  # указываем к чему применяем парсинг
                        match_name = soup.find("h1", class_="g-font-26 g-yellow g-no-margin g-inline-block").text.strip()
                        match_time = soup.find("div", class_="team-title-time__container"). \
                            find("div", class_="time").text.strip()
                        match_data = soup.find("div", class_="team-title-time__container"). \
                            find("div", class_="text").text.strip()
                        match_result = soup.find("div", class_="content-item__center"). \
                            find("span", class_="text").text.strip()

                        # проверка на наличие прогноза
                        test_data_src = soup.find("div", class_="informer-placeholder")
                        if test_data_src == None:
                            continue
                        else:
                            # вероятность игры записана в JS потому парсим его
                            data_src = soup.find("div", class_="informer-placeholder").get("data-src") # получаем ссылку на вероятность прогноза
                            link_to_probability = "https://www.footboom.com" + data_src
                            req = requests.get(link_to_probability, headers=headers)
                            probability_data = req.text
                            soup = BeautifulSoup(probability_data, "lxml")

                            match_probability = soup.find("div", class_="vote-bar vote-bar__left"). \
                                find("span").text.strip()

                            match_voices = soup.find("div", class_="vote-count"). \
                                find("span", class_="num").text.strip()

                            print(match_data, '\n', 'Время матча:', match_time, '\n', match_name, '\n', match_result, '\n'
                                  "Ставка зайдет с вероятностью:", match_probability, "\nПроанализировано ресурсов: ", match_voices, '\n'
                                  )

                            message = (str(match_data) + '\n' + 'Время матча: ' + str(match_time) + '\n' + str(match_name) + '\n' + '\n' + "*ПРОЗНОЗ*" +'\n' + str(match_result) + '\n' + '\n' +
                                  "Ставка зайдет с вероятностью: " + str(match_probability) + "\nПроанализировано ресурсов: " + str(match_voices) + '\n' )

                            send_message(message)

    if count > 2:
        with open("games_dict.json", "w") as file: # перезаписываю проверочный файл
                json.dump(games_hrefs, file, indent=4, ensure_ascii=False)

    print("Пойду спать..")
    time.sleep(900)

print("Парсинг сломан")




