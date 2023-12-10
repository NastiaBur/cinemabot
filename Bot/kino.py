from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient

from kinopoisk_unofficial.request.films.search_by_keyword_request import SearchByKeywordRequest
from kinopoisk_unofficial.request.films.film_request import FilmRequest
from kinopoisk_unofficial.request.films.seasons_request import SeasonsRequest
from kinopoisk_unofficial.request.staff.staff_request import StaffRequest

# для проверки возрастных ограничений
# ЭТО ОЧЕНЬ КРУТАЯ ФУНКЦИЯ
import re 

class Film:
    def __init__(self, name : str, type : str, year : int, directors : list, actors : list, 
                 rating : float, duration : int, poster_url : str, genre : list, country : list, 
                 description: str, short_description : str, age : int, site : str, site_url : str, is_series : bool, seasons=None):
        
        self.name = name
        self.type = type
        self.year = year
        self.directors = directors
        self.actors = actors
        self.rating = rating
        self.duration = duration # фильма/серии
        self.poster_url = poster_url
        self.genre = genre
        self.country = country
        self.description = description
        self.short_description = short_description
        self.age = age
        self.site = site
        self.site_url = site_url
        self.is_series = is_series
        self.seasons = seasons





def get_info(name):
    api_client = KinopoiskApiClient("14df4088-0c1e-475f-8295-2330a36a15ab")

    name_request = name # input()

    # get film id by name request:

    request = SearchByKeywordRequest(name_request)
    response = api_client.films.send_search_by_keyword_request(request)
    request_film_id = response.films[0].film_id
    id = FilmRequest(request_film_id)

    # get film info by id:

    film_response = api_client.films.send_film_request(id)

    # check if our request is series

    film_is_series = film_response.film.serial

    # by defolt numbers of seasons is None, so that we could make a Film object from both film ans series
    seasons_cnt = None

    # get series info by id

    if film_is_series:
        try:
            series_id = SeasonsRequest(request_film_id)
            series_response = api_client.films.send_seasons_request(series_id)

            seasons_cnt = series_response.total
            # возьмем количество эпизодов из первого сезона
            for episode in series_response.items[0].episodes:
                episodes_cnt = episode.episode_number
        except:
            client_message = "Не удалось получить количество сезонов"

    # get info about director, producer and actors
    staff_request = StaffRequest(request_film_id)
    staff_response = api_client.staff.send_staff_request(staff_request)

    staff_types = {'Переводчики', 'Композиторы', 'Сценаристы', 'Продюсеры', 'Режиссеры', 'Монтажеры', 'Режиссеры дубляжа', 'Операторы', 'Актеры', 'Художники'}

    film_directors = []
    film_actors = []
    actors_cnt = 10
    for staff in staff_response.items:
        if staff.profession_text == 'Режиссеры':
            film_directors.append(staff.name_ru)
        if staff.profession_text == 'Актеры' and actors_cnt:
            actors_cnt -= 1
            film_actors.append(staff.name_ru)


    # film info
    film_name = film_response.film.name_ru

    film_types = {"FILM" : "Фильм", "TV_SERIES" : "Сериал", "MINI_SERIES" : "Видео", "TV_SHOW" : "ТВ шоу", "VIDEO" : "Видео"}
    film_type = film_types[film_response.film.type.name]

    film_kinopoisk_rating = film_response.film.rating_kinopoisk
    film_imbd_rating = film_response.film.rating_imdb
    film_year = film_response.film.year
    film_length = film_response.film.film_length

    film_genres = []
    for genre in film_response.film.genres:
        film_genres.append(genre.genre)

    film_countries = []
    for country in film_response.film.countries:
        film_countries.append(country.country)

    film_description = film_response.film.description
    film_short_description = film_response.film.short_description
    film_poster_url = film_response.film.poster_url

    film_age = int(re.findall(r'\d+', film_response.film.rating_age_limits)[0])
    film_url = film_response.film.web_url


    film = Film(film_name, film_type, film_year, film_directors, film_actors, film_kinopoisk_rating,
                 film_length, film_poster_url, film_genres, film_countries, film_description,
                   film_short_description, film_age, "kinopoisk", film_url, film_is_series, seasons_cnt)
    return film


from urllib.request import urlopen
import json
from urllib.parse import quote

def ivi_parser(film):
  url = "https://api.ivi.ru/mobileapi/search/v7/?query=" + quote(film) + '&app_version=23801'

  response = urlopen(url)
  data = json.loads(response.read())
  rating = "Not found"
  link = None
  for i in data['result']:
      if i['title'] == film:
        rating = i['ivi_rating_10']
        link = i['share_link']
        break
  return rating, link


from urllib.parse import quote

def okko_parser(film):
  url = 'https://okko.tv/search/' + quote(film)
  return url

