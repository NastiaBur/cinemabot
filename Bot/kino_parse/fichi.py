from kinopoisk_unofficial.request.films.search_by_keyword_request import SearchByKeywordRequest
from kinopoisk_unofficial.request.films.film_request import FilmRequest
from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient

from Bot.victoria_secret import KINOPOISK_API
from Bot.logger import kino_logger



class Related_films:
    def __init__(self, name):
        self.name = name

    def get_5_films_by_name(self):
        try:
            api_client = KinopoiskApiClient(KINOPOISK_API)
            request = SearchByKeywordRequest(self.name)
            response = api_client.films.send_search_by_keyword_request(request)
        except Exception as e:
            kino_logger.critical(f'Error connecting to the kinopoisk API {e}')
            return []
        result = []
        for i in range(5):
            try:
                request_film_id = response.films[i].film_id
            except:
                break
            id = FilmRequest(request_film_id)
            try:
                film_response = api_client.films.send_film_request(id)
            except:
                film_response = None
            if film_response:
                result.append((film_response.film.name_ru, film_response.film.year))

        kino_logger.debug(f'Get {len(result) - 1} related films for {self.name}')
        return result

    def get_films(self):
        other_films_by_request = self.get_5_films_by_name()
        res = ''
        i = 1
        while i < 6 and len(other_films_by_request) > i:
            try:
                name_year = other_films_by_request[i]
            except:
                break
            print(name_year)
            if name_year[0] is not None and name_year[1] is not None:
                res += name_year[0] + ', ' + str(name_year[1]) + '\n'

            i += 1
        return res
