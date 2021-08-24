from check_url import check_url
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv
from urllib.parse import urlparse, urljoin


@check_url	
def shorten_link(token, url):
	api = "https://api-ssl.bitly.com/v4/shorten"
	header = {"Authorization": "Bearer {}".format(token)}
	body = {"long_url": url}
	response = requests.post(api, json=body, headers=header)
	response.raise_for_status()
	return response.json()["id"]


def cut_scheme(function):
	def wrapper(token, url):
		parsed_url = urlparse(url)
		if parsed_url.scheme == "https" or "http":
			new_parsed = parsed_url._replace(scheme="")
			url = new_parsed.geturl()
		value = function(token, url)
		return value
	return wrapper


@check_url
@cut_scheme
def count_clicks(token, bitlink):
	api = "https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary".format(bitlink)
	header = {"Authorization": "Bearer {}".format(token)}
	response = requests.get(api, headers=header)
	response.raise_for_status()
	return response.json()["total_clicks"]
	

@cut_scheme	
def is_bitlink(token, url):
	api = 'https://api-ssl.bitly.com/v4/bitlinks/{}'.format(url)
	header = {"Authorization": "Bearer {}".format(token)}
	response = requests.get(api, headers=header)
	return response.ok
	

def main():

	dotenv_path = join(dirname(__file__), ".env")
	load_dotenv(dotenv_path)
	token = os.getenv("TG_TOKEN")

	url = input("Введите ссылку: ")

	if is_bitlink(token, url):
		count = count_clicks(token, url)
		print("Число кликов по битлинку:", count)
	else:
		bitlink = shorten_link(token, url)
		print("Битлинк:", bitlink)
		
		
if __name__ == "__main__":
	main()


