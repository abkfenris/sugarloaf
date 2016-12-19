import requests
from bs4 import BeautifulSoup
import dateparser

from .scrape_sugarloaf_lifts_trails import update_time

URL = 'http://sugarloaf.com/the-mountain/daily-report'


def report_text(soup):
    """Returns the HTML paragraphs from the daily report"""
    report_div = soup.find('div', {'class': 'daily-report'})
    output = ''

    paragraphs = report_div.find_all('p')

    for p in paragraphs:
        output += p.decode()
    
    return output


def report_reporter(soup):
    """Returns a string with the current Snow Reporter's name"""
    report_div = soup.find('div', {'class': 'daily-report'})
    reporter = report_div.find('div', {'class': 'signature'}).find('strong')
    try:
        return reporter.contents[0]
    except AttributeError:
        return None


def make_soup():
    r = requests.get(URL)
    return BeautifulSoup(r.content, 'lxml')