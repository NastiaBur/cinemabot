# "https://api.ivi.ru/mobileapi/collection/catalog/v7/?id=14500&app_version=23801"
# posters - url
# title
# 14497 - новый год
# 11803 - истории великих женщин
# 11604 - советское
# 12076 - кино-антистресс
# 1- премия оскар
# 13556 - Все оттенки страсти
# 10938 - Фильмы-головоломки
# 12478 - Лучшее кино про животных
# 12218 - Культовое кино
# 10794 - Фильмы про средневековье

from urllib.request import urlopen
import json

collections = {
    'anti_stress' : '12076',
    'soviet' : '11604',
    'holiday' : '14497',
    'puzzle' : '10938',
    'oscar' : '1',
    'animals' : '12478',
    'women' : '11803',
    'middle_age' : '10794',
    'passion' : '13556'
    
}


def get_collections(collect):
    id = collections[collect]
    url = "https://api.ivi.ru/mobileapi/collection/catalog/v7/?id=" + id +"&app_version=23801"
    response = urlopen(url)
    data = json.loads(response.read())
    data = data['result']
    results = {}
    results[collect] = []
    count = 0
    for element in data:
        results[collect].append({'name' : element['title'], 'img' : element['posters'][0]['url']})
        count += 1
        if count == 10:
            break

    with open('Bot/collections.json', 'w') as outfile:
        json.dump(results, outfile)
