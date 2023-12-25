from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.filters_request import FiltersRequest
from kinopoisk_unofficial.model.filter_country import FilterCountry
from kinopoisk_unofficial.model.filter_order import FilterOrder
from kinopoisk_unofficial.model.filter_genre import FilterGenre
from kinopoisk_unofficial.request.films.film_search_by_filters_request import FilmSearchByFiltersRequest

from logger.logger import kino_logger
from victoria_secret import KINOPOISK_API



def get_films_by_filters(year_from=None, filter_country=None, filter_genre=None):
    """
    Fetches a list of films filtered by provided genre, country, and/or start year.

    This function queries the Kinopoisk API to retrieve a list of films based on the
    specified filters. It supports filtering by a genre, a country, and/or a start year
    (the year from which to begin the search -- year_from). The films are ordered by rating.

    If any exception occurs during API interaction, it logs the error and returns an empty list.

    :param year_from: The year to start filtering films from. Defaults to None, which means no filter by year.
    :param filter_country: The name of the country to filter the films by. Defaults to None.
    :param filter_genre: The name of the genre to filter the films by. Defaults to None.
    :return: A list of film names in Russian that match the filters, or an empty list if an error occurs.
    """
        
    try:
        api_client = KinopoiskApiClient(KINOPOISK_API)
        request = FiltersRequest()
        response = api_client.films.send_filters_request(request)
        filters_request = FilmSearchByFiltersRequest()
    except Exception as e:
        kino_logger.error(f'In get_films_by_filters exception {e} in send_filters_request')
        return []

    if filter_genre is not None:
        genres = response.genres
        for genre in genres:
            if genre.genre == filter_genre:
                filters_request.add_genre(FilterGenre(genre.id, filter_genre))

    if filter_country is not None:
        countries = response.countries
        for country in countries:
            if country.country == filter_country:
                filters_request.add_country(FilterCountry(country.id, filter_country))

    if year_from is not None:
        filters_request.year_from = year_from

    request.order = FilterOrder.RATING
    try: 
        response = api_client.films.send_film_search_by_filters_request(filters_request)
    except Exception as e:
        kino_logger.error(f'{e} in send_film_search_by_filters_request')
        return []

    films = []
    for f in response.items:
        if f.name_ru is not None:
            films.append(f.name_ru)

    return films