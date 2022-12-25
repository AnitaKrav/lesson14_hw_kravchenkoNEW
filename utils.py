import json
import sqlite3


def sql_getting(sqlite_query):
    """
    запрос к базе netflix.db
    :param sqlite_query: параметры запроса
    :return: Все данные по запросу
    """
    with sqlite3.connect("netflix.db") as connection:
        cur = connection.cursor()
        cur.execute(sqlite_query)
        executed_query = cur.fetchall()
        return executed_query


def film_research_by_title(user_title):
    """
    функция поиска фильма по названию. Отбирает самый свежий
    :param user_title: Название фильма
    :return: словарь с данными искомого фильма
    """
    sqlite_query = f"""
        SELECT title, country, listed_in, release_year, description
        FROM netflix
        WHERE title = '{user_title}'
        ORDER BY release_year DESC 
        LIMIT 1
"""
    executed_query = sql_getting(sqlite_query)
    film_dict = {}
    film_dict['title'] = executed_query[0][0]
    film_dict['country'] = executed_query[0][1]
    film_dict['release_year'] = executed_query[0][3]
    film_dict['ganre'] = executed_query[0][2]
    film_dict['description'] = executed_query[0][4]
    return film_dict


def film_research_by_years(year1, year2):
    """
    Функция поиска фильмов, выпущенных в определенные пользователем года
    :param year1: Начиная с года
    :param year2: Заканчивая годом
    :return: Список словарей с данными фильмов
    """
    sqlite_query = f"""
                    SELECT title, release_year
                    FROM netflix
                    WHERE release_year BETWEEN '{year1}' AND '{year2}'
                    ORDER BY release_year
                    LIMIT 100
                    """
    executed_query = sql_getting(sqlite_query)
    film_list = []
    film_dict = {}
    for i in executed_query:
        film_dict[i]['title'] = i[0]
        film_dict[i]['release_year'] = i[1]
        film_list.append(film_dict[i])
    return film_list


def film_research_by_rating(rating):
    """
    Подбор фильмов по рейтингу
    :param rating: указание рейтинга
    :return: список словарей с данными подхожящих фильмов
    """
    if rating == 'children':
        user_rating = 'G'
        sqlite_query = f"""
             SELECT title, rating, description
             FROM netflix
             WHERE rating = '{user_rating}'
             ORDER BY release_year
"""
    elif rating == 'family':
        user_rating = ['G', 'PG', 'PG-13']
        sqlite_query = f"""
                SELECT title, rating, description
                FROM netflix
                WHERE rating = '{user_rating[0]}' OR rating = '{user_rating[1]}' OR rating = '{user_rating[2]}'
                ORDER BY release_year
"""
    elif rating == 'adult':
        user_rating = ['R', 'NC-17']
        sqlite_query = f"""
                SELECT title, rating, description
                FROM netflix
                WHERE rating = '{user_rating[0]}' OR rating = '{user_rating[1]}' 
                ORDER BY release_year
"""
    executed_query = sql_getting(sqlite_query)
    film_list = []
    film_dict = {}
    for i in executed_query:
        film_dict[i] = {}
        film_dict[i]['title'] = i[0]
        film_dict[i]['rating'] = i[1]
        film_dict[i]['description'] = i[2]
        film_list.append(film_dict[i])
    return film_list


def film_research_by_genre(genre):
    """
    Подбор фильма по жанру
    :param genre: жанр
    :return: список словарей с данными подходящих фильмов
    """
    sqlite_query = f"""
                    SELECT title, description,listed_in
                    FROM netflix
                    WHERE listed_in LIKE '%{genre}%' 
                    ORDER BY release_year DESC 
                    LIMIT 10
                    """
    executed_query = sql_getting(sqlite_query)
    film_list = []
    film_dict = {}
    for i in executed_query:
        film_dict[i] = {}
        film_dict[i]['title'] = i[0]
        film_dict[i]['description'] = i[1]
        film_dict[i]['genre'] = i[2]
        film_list.append(film_dict[i])
    return film_list


def all_films_json():
    """
    JSON всей базы
    :return: JSON всей базы
    """
    sqlite_query = f"""
                    SELECT rating, listed_in, release_year
                    FROM netflix
"""
    executed_query = sql_getting(sqlite_query)
    return json.dumps(executed_query)
