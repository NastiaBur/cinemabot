from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.search_by_keyword_request import SearchByKeywordRequest
from kinopoisk_unofficial.request.films.film_request import FilmRequest
from kinopoisk_unofficial.request.films.seasons_request import SeasonsRequest
from kinopoisk_unofficial.request.staff.staff_request import StaffRequest
from youtube_search import YoutubeSearch
from bs4 import BeautifulSoup
import requests
from bs2json import BS2Json
import re
from urllib.request import urlopen
import json
from urllib.parse import quote
from victoria_secret import KINOPOISK_API, X_API_KEY
from logger.logger import kino_logger



class Film:
    def __init__(self, name: str):
        """
               Initialize the Film object with a given name and set up the KinopoiskApiClient.
               Attempts to find the film using the provided name and fetches its data from Kinopoisk.

               :param name: The name of the film to search for.
        """
        self.name = name
        try:
            self.api_client = KinopoiskApiClient(KINOPOISK_API)
            request = SearchByKeywordRequest(name)
            response = self.api_client.films.send_search_by_keyword_request(request)
        except Exception as e:
            kino_logger.critical(f"Error connecting to the kinopoisk API {e}")

        try:
            self.request_film_id = response.films[0].film_id
            id = FilmRequest(self.request_film_id)
            self.film_response = self.api_client.films.send_film_request(id)
        except Exception as e:
            kino_logger.error(f'Film {name} was not found, exception: {e}')
            self.film_response = None

    def get_name(self):
        """
                Get the Russian name of the film if available, otherwise its original name.

                :return: The appropriate name of the film or None if not available.
        """
        try:
            if self.film_response is None:
                return None
            if self.film_response.film.name_ru == None:
                if self.film_response.film.original_name == None:
                    return None
                return self.film_response.film.original_name
            return self.film_response.film.name_ru
        except Exception as e:
            kino_logger.error(f'Film name for {self.name} was not found, exception: {e}')
            return None

    def get_type(self):
        """
                Get the type of the film (e.g., Фильм, Сериал, Видео, ТВ шоу).

                :return: The type of the film as a string or logs an error if type is not found.
        """
        try:
            film_types = {"FILM": "Фильм", "TV_SERIES": "Сериал", "MINI_SERIES": "Видео", "TV_SHOW": "ТВ шоу",
                          "VIDEO": "Видео"}
            return film_types[self.film_response.film.type.name]
        except Exception as e:
            kino_logger.error(f'Film type for {self.name} was not found, exception: {e}')

    def get_year(self):
        """
        Get the year the film was released.

        :return: The release year of the film or logs an error if the year is not found.
        """
        try:
            return self.film_response.film.year
        except Exception as e:
            kino_logger.error(f'Film year for {self.name} was not found, exceptoin: {e}')

    def get_directors(self):
        """
        Get a list of directors of the film.

        :return: A list of directors or logs an error if no directors are found.
        """
        try:
            staff_request = StaffRequest(self.request_film_id)
            staff_response = self.api_client.staff.send_staff_request(staff_request)
            film_directors = []

            for staff in staff_response.items:
                if staff.profession_text == 'Режиссеры':
                    film_directors.append(staff.name_ru)
            return film_directors
        except Exception as e:
            kino_logger.error(f'Film directions for {self.name} was not found, exceptoin: {e}')

    def get_actors(self):
        """
        Get a list of actors in the film, up to a maximum of ten.


        :return: A list of actors or logs an error if no actors are found.
        """
        try:
            staff_request = StaffRequest(self.request_film_id)
            staff_response = self.api_client.staff.send_staff_request(staff_request)
            film_actors = []
            actors_cnt = 10
            for staff in staff_response.items:
                if staff.profession_text == 'Актеры' and actors_cnt:
                    actors_cnt -= 1
                    film_actors.append(staff.name_ru)
                    if actors_cnt == 0:
                        break
            return film_actors
        except Exception as e:
            kino_logger.error(f'Film actors for {self.name} was not found, exceptoin: {e}')

    def get_rating(self):
        """
        Get the Kinopoisk rating of the film.

        :return: The Kinopoisk rating or logs an error if the rating is not found.
        """
        try:
            return self.film_response.film.rating_kinopoisk
        except Exception as e:
            kino_logger.error(f'Film rating for {self.name} was not found, exceptoin: {e}')

    def get_duration(self):
        """
        Get the duration of the film in minutes.

        :return: The film's duration or logs an error if the duration is not found.
        """
        try:
            return self.film_response.film.film_length
        except Exception as e:
            kino_logger.error(f'Film duration for {self.name} was not found, exceptoin: {e}')

    def get_poster_url(self):
        """
        Get the URL to the film's poster.

        :return: The poster URL or logs an error if the URL is not found.
        """
        try:
            return self.film_response.film.poster_url
        except Exception as e:
            kino_logger.error(f'Film poster_url for {self.name} was not found, exceptoin: {e}')

    def get_genre(self):
        """
        Get the list of genres of the film.

        :return: A list of genres or logs an error if no genres are found.
        """
        try:
            film_genres = []
            for genre in self.film_response.film.genres:
                film_genres.append(genre.genre)
            return film_genres
        except Exception as e:
            kino_logger.error(f'Film genre for {self.name} was not found, exceptoin: {e}')

    def get_country(self):
        """
        Get the list of countries associated with the film.

        :return: A list of countries or logs an error if no countries are found.
        """
        try:
            film_countries = []
            for country in self.film_response.film.countries:
                film_countries.append(country.country)
            return film_countries
        except Exception as e:
            kino_logger.error(f'Film country for {self.name} was not found, exceptoin: {e}')

    def get_description(self):
        """
        Get the full description of the film.

        :return: The full description or logs an error if the description is not found.
        """
        try:
            return self.film_response.film.description
        except Exception as e:
            kino_logger.error(f'Film description for {self.name} was not found, exceptoin: {e}')

    def get_short_description(self):
        """
        Get the short description of the film.

        :return: The short description or logs an error if the short description is not found.
        """
        try:
            return self.film_response.film.short_description
        except Exception as e:
            kino_logger.error(f'Film short_description for {self.name} was not found, exceptoin: {e}')

    def get_age(self):
        """
        Get the age limit for the film.

        :return: The age limit as an integer or log a warning if no age limit is found and return "-".
        """
        try:
            age = int(re.findall(r'\d+', self.film_response.film.rating_age_limits)[0])
        except Exception as e:
            kino_logger.warning(f'No age for fim {self.name}, exception: {e}')
            age = "-"
        return age


    def get_kinopoisk_url(self):
        """
        Get the Kinopoisk URL for the film.

        :return: The Kinopoisk web URL or logs an error if the URL is not found.
        """
        try:
            return self.film_response.film.web_url
        except Exception as e:
            kino_logger.error(f'Film kinopoisk_url for {self.name} was not found, exceptoin: {e}')

    def is_series(self):
        """
        Determine if the film is a series.

        :return: True if the film is a series, False otherwise or logs a warning if the information is not found.
        """
        try:
            return self.film_response.film.serial
        except Exception as e:
            kino_logger.warning(f'Film is_series for {self.name} was not found, exceptoin: {e}')

    def get_seasons(self):
        """
        If the film is a series, get the number of seasons available.

        :return: The number of seasons or logs an error if not applicable or could not be found.
        """
        seasons_cnt = None
        if self.is_series():
            try:
                series_id = SeasonsRequest(self.request_film_id)
                series_response = self.api_client.films.send_seasons_request(series_id)
                seasons_cnt = series_response.total
            except Exception as e:
                kino_logger.warning(f'Film seasons for {self.name} were not found , exception: {e}')
        return seasons_cnt

    def get_external_sources(self, source):
        """
        Get the external source link for the film.

        :param source: The name of the external source platform (e.g., Okko, Wink).
        :return: The external source URL or logs an error if the information could not be retrieved.
        """
        # Okko, Wink
        url = 'https://kinopoiskapiunofficial.tech/api/v2.2/films/' + str(
            self.request_film_id) + '/external_sources?page=1'
        payload = {'Content-Type': 'application/json', 'X-API-KEY': X_API_KEY}
        r = requests.get(url, headers=payload)
        status = r.status_code
        if status != 200:
            kino_logger.error(f'API kinopoisk externel_sources status is not 200')
            return None
        try:
            data = r.json()
            link = None
            for platform in data['items']:
                if platform['platform'] == source:
                    link = platform['url']
        except Exception as e:
            kino_logger.warning(f"Some troubles with {source} in kinipoisk, \n exception: {e}")
            return None
        return link

    def get_ivi_info(self):
        """
        Get the IVI rating and link for the film.

        :return: A tuple containing the IVI rating and share link, or log an error if the film is not found on IVI.
        """
        try:
            url = "https://api.ivi.ru/mobileapi/search/v7/?query=" + quote(self.get_name()) + '&app_version=23801'
            response = urlopen(url)
            data = json.loads(response.read())
        except Exception as e:
            kino_logger.error(f'Film {self.get_name()} was not found on ivi')
            return None, None
        rating = "Not found"
        link = None
        for i in data['result']:
            if i['title'] == self.get_name():
                try:
                    rating = i['ivi_rating_10']
                except:
                    kino_logger.warning(f'No ivi rating for {self.get_name()}')
                try:
                    link = i['share_link']
                except:
                    kino_logger.warning(f'No ivi link for {self.get_name()}')
                break

        return rating, link

    def youtube_parser(self):
        """
        Search YouTube for a trailer of the film and return the first result.


        :return: The YouTube URL of the trailer or logs a warning if the search fails.
        """
        try:
            res = YoutubeSearch(self.get_name() + ' trailer', max_results=1).to_dict()
            return 'https://www.youtube.com' + res[0]['url_suffix']
        except Exception as e:
            kino_logger.warning(f'Some troubles with youtube for {self.get_name()}, exception:{e}')

    def anime_parser(self):
        """
        Parse for anime-related information for the film from AnimeGo.

        :return: The AnimeGo URL for the anime if the film is an anime or logs an error if not found.
        """
        genres = self.get_genre()

        if genres.count('аниме') > 0:
            url = "https://animego.org/search/all?q=" + quote(self.get_name()) + '/'
            page = requests.get(url)
            status = page.status_code
            if status != 200:
                kino_logger.error(f'Animego status is not 200')
                return None
            soup = BeautifulSoup(page.text, "lxml")
            try:
                href = soup.find('main').find('a', class_="d-block")['href']
            except Exception as e:
                href = None
                kino_logger.warning(f'No anime for {self.get_name()}')
                return href
        return None

    def zona_parser(self):
        """
        Parse for the film information from Zona.

        :return: The Zona URL for the film or logs an error if the film is not found on Zona.
        """
        url = 'https://w140.zona.plus/search/' + quote(self.get_name())
        response = requests.get(url)
        if response.status_code != 200:
            kino_logger.error(f'Zona status is not 200')
            return None
        bs = BeautifulSoup(response.text, "lxml")
        temp = bs.find('ul', {"class": 'results'})
        if temp:
            bs2json = BS2Json(temp)
            json_obj = bs2json.convert()
            for i in range(len(json_obj['ul']['li'])):
                name = ''
                year = ''
                try:
                    name = json_obj['ul']['li'][i]['a']['div'][1]['div']['text']
                    try:
                        year = json_obj['ul']['li'][i]['a']['div'][1]['span'][1]['text']
                    except:
                        year = json_obj['ul']['li'][i]['a']['div'][1]['span']['text']
                except:
                    pass
                if name == self.get_name() and int(year) == self.get_year():
                    return ('https://w140.zona.plus' + json_obj['ul']['li'][i]['a']['attrs']['href'])
        else:
            kino_logger.warning(f'No zona films for {self.get_name()}')
        return None
