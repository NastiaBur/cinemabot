from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.filters_request import FiltersRequest
from kinopoisk_unofficial.model.filter_country import FilterCountry
from kinopoisk_unofficial.model.filter_order import FilterOrder
from kinopoisk_unofficial.model.filter_genre import FilterGenre
from kinopoisk_unofficial.request.films.film_search_by_filters_request import FilmSearchByFiltersRequest

from logger.logger import kino_logger
from victoria_secret import KINOPOISK_API



def get_films_by_filters(year_from=None, filter_country=None, filter_genre=None):


    if filter_genre is not None:
        filter_genre = filter_genre.lower()
    print(year_from, filter_country, filter_genre)
    api_client = KinopoiskApiClient(KINOPOISK_API)
    request = FiltersRequest()
    response = api_client.films.send_filters_request(request)
    filters_request = FilmSearchByFiltersRequest()

    if filter_genre is not None:
        genres = response.genres
        genre_id = None
        print(filter_genre)
        for genre in genres:
            if genre.genre == filter_genre:
                print(genre.genre)
                genre_id = genre.id
                print(genre_id)
                filters_request.add_genre(FilterGenre(genre_id, filter_genre))

    if filter_country is not None:
        countries = response.countries
        country_id = None
        for country in countries:
            if country.country == filter_country:
                country_id = country.id
                filters_request.add_country(FilterCountry(country_id, filter_country))

    if year_from is not None:
        filters_request.year_from = year_from
    request.order = FilterOrder.RATING

    response = api_client.films.send_film_search_by_filters_request(filters_request)
    films = []
    for f in response.items:
        films.append(f.name_ru)
    return films