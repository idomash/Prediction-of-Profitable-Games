import requests as req
from bs4 import BeautifulSoup as bs
import json
import time as t

DATABASE_NAME = "database.json"

GENRES = [
    'Action', 'Action-Adventure', 'Adventure',
    'Board Game',
    'Education',
    'Fighting',
    'Misc', 'MMO', 'Music',
    'Party', 'Platform', 'Puzzle',
    'Racing', 'Role-Playing',
    'Sandbox', 'Shooter', 'Simulation', 'Sports', 'Strategy',
    'Visual Novel'
]


def load_database():
    # Loading "database"
    with open(DATABASE_NAME, 'r') as data_json:
        json_data = json.load(data_json)
    return json_data


def save_data(data):
    json_data = load_database()
    # Appending to the existing data
    json_data.append(data)
    # Saving the database with the added data
    with open(DATABASE_NAME, 'w') as new_update:
        json.dump(json_data, new_update, indent=4)


def get_amount_of_data_collected():
    data = load_database()
    return len(data)


def load_page(genre, page_number):
    """
    This function will try to load the page.
    if the page loads, it will return the HTML object
    else - will retry.
    """
    print('Loading')
    url = f"https://www.vgchartz.com/games/games.php?page={page_number}&results=200&genre={genre}&order=Sales&ownership=Both&direction=DESC&showtotalsales= \
1&shownasales=1&showpalsales=1&showjapansales=1&showothersales=1&showpublisher \
=0&showdeveloper=1&showreleasedate=1&showlastupdate=0& \
showvgchartzscore=0&showcriticscore=0&showuserscore=0&showshipped=1"
    response = req.get(url)
    # If response is valid:
    if "503 Service Unavailable" not in str(response.content) and response.status_code == 200:
        print(f'{response.status_code} | Connected!')
        return response.content
    else:
        # Trying again to get the page again
        print(f'{response.status_code} - Could not connect! Will retry in 20 seconds')
        t.sleep(20)
        return load_page(genre, page_number)




def parse_html_page(genre, html_object):
    """
    This function gets the HTML object which was loaded on load_page.
    and extracts the data from it.
    """
    try:
        soup = bs(html_object, "html.parser")
        table = soup.find('div', id='generalBody').find_all('tr')
        if len(table) > 5:
            # Removing headers we don't need
            del table[:3]
            del table[-1]
            for game in table:
                # Loading all the content per header per game
                row = game.find_all('td')
                game_record = {
                    'name': row[2].text,        'developer': row[4].text,
                    'platform': row[3].find('img')['alt'],
                    'genre': genre,             'total_shipments': row[5].text,
                    'total_sales': row[6].text, 'na_sales': row[7].text,
                    'pal_sales': row[8].text,   'japan_sales': row[9].text,
                    'other_sales': row[10].text, 'release': row[11].text
                }
                # Saving data after successfully parsing
                save_data(game_record)
            return True
        return False
    except Exception as e:
        return False


# Starting point of the code
if __name__ == "__main__":
    progress_counter, games_counter = 0, 0
    for g in GENRES:
        for page in range(45):
            progress_counter += 1
            data = load_page(g, page)
            status = parse_html_page(g, data)
            if status:
                games_counter += 200
                print(f'PROGRESS: {progress_counter}/{14 * len(GENRES)}/ Genre:{g}')
            else:
                break
