import requests

# todo: make parallel & async 
def download(page_url: str):
    return requests.get(page_url)