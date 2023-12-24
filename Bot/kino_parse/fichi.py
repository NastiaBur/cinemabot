from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.search_by_keyword_request import SearchByKeywordRequest
from kinopoisk_unofficial.request.films.film_request import FilmRequest
from kinopoisk_unofficial.request.films.film_top_request import FilmTopRequest
from kinopoisk_unofficial.model.dictonary.top_type import TopType

from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient

from kinopoisk_unofficial.model.filter_country import FilterCountry
from kinopoisk_unofficial.model.filter_genre import FilterGenre
from kinopoisk_unofficial.request.films.film_search_by_filters_request import FilmSearchByFiltersRequest

from victoria_secret import KINOPOISK_API

def get_top_films():
    api_client = KinopoiskApiClient(KINOPOISK_API)
    request = FilmTopRequest(TopType.TOP_100_POPULAR_FILMS)
    response = api_client.films.send_film_top_request(request)
    
def get_films_by_filters(year_from=None, filter_country=None, filter_genre=None):
    
    api_client = KinopoiskApiClient(KINOPOISK_API)
    filters_request = FilmSearchByFiltersRequest()
   
    filters_request.year_from = year_from
    filters_request.add_genre(FilterGenre(1, filter_genre))
    filters_request.add_country(FilterCountry(1, filter_country))

    response = api_client.films.send_film_search_by_filters_request(filters_request)
    films = []
    for f in response.items:
        films.append(f.name_ru)
    return films


def get_5_films_by_name(name):
    api_client = KinopoiskApiClient(KINOPOISK_API)
    request = SearchByKeywordRequest(name)
    response = api_client.films.send_search_by_keyword_request(request)
    result = []
    for i in range(5):
        request_film_id = response.films[i].film_id 
        id = FilmRequest(request_film_id)
        try:
            film_response = api_client.films.send_film_request(id)
        except:
            film_response = None
        if film_response:
            result.append((film_response.film.name_ru, film_response.film.year))
    return result


def create_str_list(name):
    other_films_by_request = get_5_films_by_name(name)
    res = ''
    i = 1
    while i < 6 and len(other_films_by_request) > i:
        name_year = other_films_by_request[i]
        print(name_year)
        print(other_films_by_request)
        res += name_year[0] + ', ' + str(name_year[1]) + '\n'
        i += 1
    return res
