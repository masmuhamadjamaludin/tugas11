import requests

api_key = '2ef83c94-9560-4ae3-b1a0-62dc81ee4581'
word = 'potato'
url = f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}'

res = requests.get(url)

definitions = res.json()

for definition in definitions:
    print(definitions)