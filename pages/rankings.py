from __future__ import division
from bs4 import BeautifulSoup

import downloader
from models.ranking import Ranking
from db.data_inserter import get_database

RANKINGS_URL = "https://www.ufc.com/rankings"

def populate_rankings():
    db = get_database()
    db.connect()
    rankings_page = downloader.download(RANKINGS_URL)
    groups_html = get_html_by_group(rankings_page)
    for html in groups_html[1:]:
        ranking = get_ranking_from_html(html)
        db.add_fighter_from_ranking(ranking)

def get_ranking_from_html(html):
    division_name = html.find_all("h4")[0].text.strip()
    fighter_divs = html.find_all("div", {"class": "views-row"})
    fighters = [fighter_div.text.strip() for fighter_div in fighter_divs]
    ranking = Ranking(division_name, fighters)
    return ranking

def get_html_by_group(rankings_page):
    RELEVANT_CLASS = "view-grouping"
    rankings_html = rankings_page.text
    soup = BeautifulSoup(rankings_html, 'html.parser')
    return soup.find_all("div", {"class": RELEVANT_CLASS})
    