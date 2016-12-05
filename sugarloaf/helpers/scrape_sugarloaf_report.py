import warnings

import requests
from bs4 import BeautifulSoup
import dateparser

URL = 'http://sugarloaf.com/the-mountain/daily-report'

def update_time(soup):
    """Returns datetime when the lift and trail report was last updated"""
    right_content = soup.find('div', {'class': 'content--right'})
    condition_update_string = right_content.find('small').contents[0]
    condition_time_string = condition_update_string.strip().split('of')[1]
    return dateparser.parse(condition_time_string)


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