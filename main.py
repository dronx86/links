import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv


def shorten_link(token, url):
	api = "https://api-ssl.bitly.com/v4/shorten"
	header = {"Authorization": "Bearer {}".format(token)}
	body = {"long_url": url}
	response = requests.post(api, json=body, headers=header)
	response.raise_for_status()
	return response.json()["id"]


def count_clicks(token, bitlink):
	api = "https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary".format(bitlink)
	header = {"Authorization": "Bearer {}".format(token)}
	response = requests.get(api, headers=header)
	response.raise_for_status()
	return response.json()["total_clicks"]
	

def is_bitlink(token, cuted_url):
	url = "https://" + cuted_url
	url_check = requests.get(url)
	url_check.raise_for_status()
	api = "https://api-ssl.bitly.com/v4/bitlinks/{}".format(cuted_url)
	header = {"Authorization": "Bearer {}".format(token)}
	response = requests.get(api, headers=header)
	return response.ok
	

def main():

	dotenv_path = join(dirname(__file__), ".env")
	load_dotenv(dotenv_path)
	token = os.getenv("TG_TOKEN")

	url = input("Введите ссылку: ")
	if url[:8] == "https://":
		cuted_url = url[8:]
	elif url[:7] == "http://":
		cuted_url = url[7:]
	else:
		cuted_url = url

	try:
		if is_bitlink(token, cuted_url):
			count = count_clicks(token, cuted_url)
			print("Число кликов по битлинку:", count)
		else:
			bitlink = shorten_link(token, url)
			print("Битлинк:", bitlink)
	except requests.exceptions.HTTPError:
		raise SystemExit("Некорректная ссылка!")
		
		
if __name__ == "__main__":
	main()
