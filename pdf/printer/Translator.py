import requests
import json

class Translator:
	def translate(self, text, language):
		url = "https://google-translate113.p.rapidapi.com/api/v1/translator/text"

		payload = {
			"from": "en",
			"to": language,
			"text": text
		}
		headers = {
			"content-type": "application/x-www-form-urlencoded",
			"X-RapidAPI-Key": "eaf0b9c8e4mshe708e130bc51211p1ef21bjsnaba4c578bfb3",
			"X-RapidAPI-Host": "google-translate113.p.rapidapi.com"
		}

		response = requests.post(url, data=payload, headers=headers)

		return (response.json()['trans'])