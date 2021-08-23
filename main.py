import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv

	
def shorten_link(token, url):
	api = 'https://api-ssl.bitly.com/v4/shorten'
	header = {'Authorization': 'Bearer {}'.format(token)}
	body = {'long_url': url}
	response = requests.post(api, json=body, headers=header)
	response.raise_for_status()
	return response.json()['id']
	

def count_clicks(token, bitlink):
	api = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'.format(bitlink)
	header = {'Authorization': 'Bearer {}'.format(token)}
	response = requests.get(api, headers=header)
	response.raise_for_status()
	return response.json()['total_clicks']
	
	
def is_bitlink(token, url):
	api = 'https://api-ssl.bitly.com/v4/bitlinks/{}'.format(url)
	header = {'Authorization': 'Bearer {}'.format(token)}
	response = requests.get(api, headers=header)
	try:
		response.raise_for_status()
	except requests.exceptions.HTTPError:
		return False
	return True
	

def main():

	dotenv_path = join(dirname(__file__), '.env')
	load_dotenv(dotenv_path)
	token = os.getenv("TOKEN")
			
	url = input('Введите ссылку: ')
	if is_bitlink(token, url):
		try:
			count = count_clicks(token, url)
		except requests.exceptions.HTTPError:
			raise SystemExit("Некорректная ссылка!")
		print('Количество кликов:', count)
	else:
		try:
			bitlink = shorten_link(token, url)
		except requests.exceptions.HTTPError:
			raise SystemExit("Некорректная ссылка!")
		print('Битлинк', bitlink)
		
		
if __name__ == "__main__":
	main()


