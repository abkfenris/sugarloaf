import requests
from bs4 import BeautifulSoup
import dateparser

URL = 'http://sugarloaf.com/the-mountain/trails-and-lifts'


def trail_name(trail):
    """Returns a string containing the name of the trail"""
    try:
        return trail.contents[0]
    except AttributeError:
        raise AttributeError(trail)


def trail_status(trail):
    """Returns True if the trail is open"""
    if 'closed' in trail.attrs['class'] or 'snowmaking-closed' in trail.attrs['class']:
        return False
    return True

def trail_snowmaking(trail):
    """Returns true if snowmaking in progress"""
    if 'snowmaking-closed' in trail.attrs['class'] or 'snowmaking-open' in trail.attrs['class']:
        return True
    return False

dificulty = {'beginner', 'intermediate', 'double-black', 'black', 'terrain-park'}


def trail_difficulty(trail):
    """Returns a string with the difficulty of given trail"""
    dif = set(trail.attrs['class']).intersection(dificulty)
    try:
        return list(dif)[0]
    except IndexError:
        raise IndexError(trail)


def trail_groomed(trail):
    """Returns true if the trail has been groomed"""
    if 'groomed' in trail.attrs['class']:
        return True
    return False


def trail_terrain_park(trail):
    """Returns True if the trail is a terrain park"""
    if 'terrain-park' in trail.attrs['class']:
        return True
    return False


def trail_area(trail):
    """Returns a string with the area of the mountain the trail is in"""
    try:
        return trail.find_previous_sibling('h3').contents[0]
    except AttributeError:
        raise AttributeError(trail)


def update_trails(soup):
    """Yields dicts with Sugarloaf trails names, current status, and other attributes"""
    

    trail_status_div = soup.find('div', {'class': 'trail-status'})

    all_trail_divs = trail_status_div.find_all('div', {'class', 'trail'})

    for trail_div in all_trail_divs:
        yield {
            'name': trail_name(trail_div),
            'open': trail_status(trail_div),
            'difficulty': trail_difficulty(trail_div),
            'groomed': trail_groomed(trail_div),
            'terrain-park': trail_terrain_park(trail_div),
            'area': trail_area(trail_div),
            'snowmaking': trail_snowmaking(trail_div)
        }


def lift_name(lift):
    """Returns a string with the lifts name"""
    return lift.contents[0]


statuses = {'open', 'closed', 'scheduled', 'hold'}


def lift_status(lift):
    """Returns the lift status"""
    status = set(lift.attrs['class']).intersection(statuses)
    try:
        return list(status)[0]
    except IndexError:
        raise IndexError(lift)

def update_lifts(soup):
    """Yields dicts with Sugarloaf lift names and statuses"""
    div_lift_status = div_trail_status = soup.find('div', {'class': 'lift-status'})
    lifts_divs = div_lift_status.find_all('div', {'class': 'lift'})

    for lift_div in lifts_divs:
        yield {
            'name': lift_name(lift_div),
            'status': lift_status(lift_div)
        }


def update_time(soup):
    """Returns datetime when the lift and trail report was last updated"""
    right_content = soup.find('div', {'class': 'content--right'})
    condition_update_string = right_content.find('small').contents[0]
    condition_time_string = condition_update_string.strip().split('of')[1]
    return dateparser.parse(condition_time_string)


def make_soup():
    """Returns BeautifulSoup for lifts and trails"""
    r = requests.get(URL)
    return BeautifulSoup(r.content, 'lxml')


if __name__ == '__main__':
    import json

    soup = make_soup()

    trails = list(update_trails(soup))

    lifts = list(update_lifts(soup))

    all_statuses = {'trails': trails, 
                    'lifts': lifts, 
                    'update datetime': update_time(soup).isoformat()}

    with open('sugarloaf.json', 'w') as f:
        json.dump(all_statuses, f)