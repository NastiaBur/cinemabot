
from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.search_by_keyword_request import SearchByKeywordRequest
from kinopoisk_unofficial.request.films.film_request import FilmRequest
from kinopoisk_unofficial.request.films.seasons_request import SeasonsRequest
from kinopoisk_unofficial.request.staff.staff_request import StaffRequest
from kinopoisk_unofficial.request.films.film_top_request import FilmTopRequest
from kinopoisk_unofficial.model.dictonary.top_type import TopType

from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.related_film_request import RelatedFilmRequest

from youtube_search import YoutubeSearch

from bs4 import BeautifulSoup
import requests
import json
from bs2json import BS2Json
from urllib.parse import quote

import re 
from urllib.request import urlopen
import json
from urllib.parse import quote
from victoria_secret import KINOPOISK_API



class Film:
    def __init__(self, name : str):

        self.api_client = KinopoiskApiClient(KINOPOISK_API)
        request = SearchByKeywordRequest(name)
        response = self.api_client.films.send_search_by_keyword_request(request)
        try:
            self.request_film_id = response.films[0].film_id 
            id = FilmRequest(self.request_film_id)
            self.film_response = self.api_client.films.send_film_request(id)
        except:
            self.film_response = None
    
    
    def get_name(self):
        if self.film_response is None:
            return None
        return self.film_response.film.name_ru

    def get_type(self):
        film_types = {"FILM" : "Фильм", "TV_SERIES" : "Сериал", "MINI_SERIES" : "Видео", "TV_SHOW" : "ТВ шоу", "VIDEO" : "Видео"}
        return film_types[self.film_response.film.type.name]

    def get_year(self):
        return self.film_response.film.year

    def get_directors(self):
        staff_request = StaffRequest(self.request_film_id)
        staff_response = self.api_client.staff.send_staff_request(staff_request)
        film_directors = []
       
        for staff in staff_response.items:
            if staff.profession_text == 'Режиссеры':
                film_directors.append(staff.name_ru)
        return film_directors
    
    def get_actors(self):
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

    def get_rating(self):
        return self.film_response.film.rating_kinopoisk
    
    def get_duration(self):
        return self.film_response.film.film_length
    
    def get_poster_url(self):
        return self.film_response.film.poster_url
    
    def get_genre(self):
        film_genres = []
        for genre in self.film_response.film.genres:
            film_genres.append(genre.genre)
        return film_genres

    def get_country(self):
        film_countries = []
        for country in self.film_response.film.countries:
            film_countries.append(country.country)
        return film_countries

    def get_description(self):
        return self.film_response.film.description

    def get_short_description(self):
        return self.film_response.film.short_description

    def get_age(self):
        try:
            age = int(re.findall(r'\d+', self.film_response.film.rating_age_limits)[0])
        except:
            age = "I think you can watch"
        return age

    def get_kinopoisk_url(self):
        return self.film_response.film.web_url

    def is_series(self):
        return self.film_response.film.serial

    def get_seasons(self):
        seasons_cnt = None
        if self.is_series():
            try:
                series_id = SeasonsRequest(self.request_film_id)
                series_response = self.api_client.films.send_seasons_request(series_id)
                seasons_cnt = series_response.total
            except:
                pass
        return seasons_cnt
    

    def get_related_films(self):
        related_request = RelatedFilmRequest(self.request_film_id)
        related_response = self.api_client.films.send_related_film_request(related_request)
        films = []
        for f in related_response.items:
            films.append(f.name_ru)
        return films
    

    def get_ivi_info(self):
        url = "https://api.ivi.ru/mobileapi/search/v7/?query=" + quote(self.get_name()) + '&app_version=23801'
        response = urlopen(url)
        data = json.loads(response.read())
        rating = "Not found"
        link = None
        for i in data['result']:
            if i['title'] == self.get_name():
                rating = i['ivi_rating_10']
                link = i['share_link']
                break
            
        return rating, link
    
    def youtube_parser(self):
        res = YoutubeSearch(self.get_name() + ' trailer', max_results = 1).to_dict()
        return 'https://www.youtube.com' + res[0]['url_suffix']


    def lordfilm_parser(self):
        url = "https://hd.10rdfilm.online/search/" + quote(self.get_name()) + '/'
        page = requests.get(url)
        status = page.status_code
        if status != 200:
            return None
        soup = BeautifulSoup(page.text, "lxml")
        try:
            href = soup.find('main').find('a', class_="th-in with-mask")['href']
        except:
            href = None
        return href

    def anime_parser(self):
        genres = self.get_genre()

        if genres.count('аниме') > 0:
            url = "https://animego.org/search/all?q=" + quote(self.get_name()) + '/'
            page = requests.get(url)
            status = page.status_code
            if status != 200:
                return None
            soup = BeautifulSoup(page.text, "lxml")
            try:
                href = soup.find('main').find('a', class_="d-block")['href']
            except:
                href = None
            return href
        return None
    
    def zona_parser(self):
        url = 'https://w140.zona.plus/search/' + quote(self.get_name())
        response = requests.get(url)
        bs = BeautifulSoup(response.text, "lxml")
        temp = bs.find('ul', {"class" : 'results'})
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
        return None

from urllib.parse import quote

def okko_parser(film):
  url = 'https://okko.tv/search/' + quote(film)
  return url


def get_top_films():
    api_client = KinopoiskApiClient(KINOPOISK_API)
    request = FilmTopRequest(TopType.TOP_100_POPULAR_FILMS)
    #request.type = TopType.TOP_100_POPULAR_FILMS
    response = api_client.films.send_film_top_request(request)
    