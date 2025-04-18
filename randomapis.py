import requests
import json

word = 'stupendous'
response = requests.get(f'https://random-word-api.p.rapidapi.com/L/7')
content = json.loads(response.content.decode("utf-8"))
# meaning = content[0]['meanings'][0]['definitions'][0]['definition']

word = 
# print(f"{word} : {meaning}")

print(content)