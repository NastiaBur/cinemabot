from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.film_request import FilmRequest

from kinopoisk_unofficial.request.films.search_by_keyword_request import SearchByKeywordRequest

# для проверки возрастных ограничений
import re 

class Film:
    def __init__(self, name : str, year : int, rating : float, duration : int, genre : list, country : list, description : str, age : int, site : str):
        self.name = name
        self.year = year
        self.rating = rating
        self.duration = duration
        self.genre = genre
        self.country = country
        self.description = description
        self.age = age
        self.site = site

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

    film_name = film_response.film.name_ru
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

    film_description = film_response.film.short_description

    film_age = int(re.findall(r'\d+', film_response.film.rating_age_limits)[0])


    film = Film(film_name, film_year, film_kinopoisk_rating, film_length, film_genres, film_countries, film_description, film_age, "kinopoisk")
    return film