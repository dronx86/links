import requests

def check_url(function):
    def wrapper(token, url):
        try:
            value = function(token, url)
        except requests.exceptions.HTTPError:
            raise SystemExit("Некорректная ссылка!")
        return value
    return wrapper