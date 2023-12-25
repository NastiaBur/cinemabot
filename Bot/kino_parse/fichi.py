from kinopoisk_unofficial.request.films.search_by_keyword_request import SearchByKeywordRequest
from kinopoisk_unofficial.request.films.film_request import FilmRequest
from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient

from victoria_secret import KINOPOISK_API
from logger.logger import kino_logger



class Related_films:
    """
    A class to find films related to a given name from the Kinopoisk API.
    
    This class queries the Kinopoisk API to fetch details of films that are related
    to the search keyword provided during class instantiation.
    
    Attributes:
        name (str): The keyword name to search for related films.
    """

    def __init__(self, name):
        """
        Initializes the Related_films class with the specified film name.
        
        :param name: A string representing the keyword to search for related films.
        """
        self.name = name

    def get_5_films_by_name(self):
        """
        Retrieves up to five films related to the keyword name from the Kinopoisk API.
        
        This method searches for films by keyword and fetches the details of the first 
        five search results. It is designed to handle and log exceptions if there are 
        issues connecting to the API or retrieving film data.
        
        :return: A list of tuples, where each tuple contains the film name and year.
                 Returns an empty list if there are exceptions or no data.
        """
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
            except IndexError:
                break  # Stop if there are fewer than 5 films
            
            id = FilmRequest(request_film_id)
            try:
                film_response = api_client.films.send_film_request(id)
            except Exception as e:
                kino_logger.error(f'Error retrieving film details: {e}')
                continue  # Skip to the next film
            
            if film_response:
                result.append((film_response.film.name_ru, film_response.film.year))

        kino_logger.debug(f'Got {len(result)} related films for "{self.name}"')
        return result

    def get_films(self):
        """
        Constructs a string with the names and years of up to five related films.
        
        This method gets up to five related films using the `get_5_films_by_name`
        method and constructs a string listing the films, each on a new line.
        
        :return: A string representing the list of related films by name and year,
                 separated by commas. Empty if no related films are found or if an
                 error occurs.
        """
        other_films_by_request = self.get_5_films_by_name()
        res = ''
        i = 1
        while i < 6 and i < len(other_films_by_request):
            name_year = other_films_by_request[i]

            if name_year[0] is not None and name_year[1] is not None:
                res += f'{name_year[0]}, {str(name_year[1])}\n'

            i += 1
        
        return res.strip()  # Remove any trailing newline characters
