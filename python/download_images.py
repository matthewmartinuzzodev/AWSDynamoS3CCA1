import requests
import json

with open("a1.json") as music_data_file:
    music_data = json.load(music_data_file)["songs"]
for music_detail in music_data:
    title = music_detail["title"]
    img_url = music_detail["img_url"]
    img_data = requests.get(img_url).content
    with open("images/" + title + ".jpg", 'wb+') as handler:
        handler.write(img_data)

