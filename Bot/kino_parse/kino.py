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
from victoria_secret import KINOPOISK_API
from logger import kino_logger



class Film:
    def __init__(self, name: str):
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
        try:
            if self.film_response is None:
                return None
            return self.film_response.film.name_ru
        except Exception as e:
            kino_logger.error(f'Film name for {self.name} was not found, exception: {e}')
            return None

    def get_type(self):
        try:
            film_types = {"FILM": "Фильм", "TV_SERIES": "Сериал", "MINI_SERIES": "Видео", "TV_SHOW": "ТВ шоу",
                          "VIDEO": "Видео"}
            return film_types[self.film_response.film.type.name]
        except Exception as e:
            kino_logger.error(f'Film type for {self.name} was not found, exception: {e}')

    def get_year(self):
        try:
            return self.film_response.film.year
        except Exception as e:
            kino_logger.error(f'Film year for {self.name} was not found, exceptoin: {e}')

    def get_directors(self):
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
        try:
            return self.film_response.film.rating_kinopoisk
        except Exception as e:
            kino_logger.error(f'Film rating for {self.name} was not found, exceptoin: {e}')

    def get_duration(self):
        try:
            return self.film_response.film.film_length
        except Exception as e:
            kino_logger.error(f'Film duration for {self.name} was not found, exceptoin: {e}')

    def get_poster_url(self):
        try:
            return self.film_response.film.poster_url
        except Exception as e:
            kino_logger.error(f'Film poster_url for {self.name} was not found, exceptoin: {e}')

    def get_genre(self):
        try:
            film_genres = []
            for genre in self.film_response.film.genres:
                film_genres.append(genre.genre)
            return film_genres
        except Exception as e:
            kino_logger.error(f'Film genre for {self.name} was not found, exceptoin: {e}')

    def get_country(self):
        try:
            film_countries = []
            for country in self.film_response.film.countries:
                film_countries.append(country.country)
            return film_countries
        except Exception as e:
            kino_logger.error(f'Film country for {self.name} was not found, exceptoin: {e}')

    def get_description(self):
        try:
            return self.film_response.film.description
        except Exception as e:
            kino_logger.error(f'Film description for {self.name} was not found, exceptoin: {e}')

    def get_short_description(self):
        try:
            return self.film_response.film.short_description
        except Exception as e:
            kino_logger.error(f'Film short_description for {self.name} was not found, exceptoin: {e}')

    def get_age(self):
        try:
            age = int(re.findall(r'\d+', self.film_response.film.rating_age_limits)[0])
        except Exception as e:
            kino_logger.warning(f'No age for fim {self.name}, exception: {e}')
            age = "-"
        return age

    def get_kinopoisk_url(self):
        try:
            return self.film_response.film.web_url
        except Exception as e:
            kino_logger.error(f'Film kinopoisk_url for {self.name} was not found, exceptoin: {e}')

    def is_series(self):
        try:
            return self.film_response.film.serial
        except Exception as e:
            kino_logger.warning(f'Film is_series for {self.name} was not found, exceptoin: {e}')

    def get_seasons(self):
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
        # Okko, Wink
        url = 'https://kinopoiskapiunofficial.tech/api/v2.2/films/' + str(
            self.request_film_id) + '/external_sources?page=1'
        payload = {'Content-Type': 'application/json', 'X-API-KEY': '4ab268be-1ff8-4bcd-bda8-85d7afb10819'}
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
        try:
            res = YoutubeSearch(self.get_name() + ' trailer', max_results=1).to_dict()
            return 'https://www.youtube.com' + res[0]['url_suffix']
        except Exception as e:
            kino_logger.warning(f'Some troubles with youtube for {self.get_name()}, exception:{e}')

    def anime_parser(self):
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


