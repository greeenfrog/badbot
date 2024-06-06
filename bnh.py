import requests
from bs4 import BeautifulSoup


def get_courts(date_string, site_id=2):
    url = 'https://book.bnh.org.nz/'
    params = {
        'dateString': date_string, # '06-Jun-2024'
        'siteId': site_id,
    }
    r = requests.get(url, params)

    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('div', {'id': 'court-table'})
    if table is None:
        return

    courts = {}
    for tr in table.find_all('tr'):
        header = tr.find('td', {'class': 'header'})
        if not header:
            continue
        hour = header.get_text(strip=True).replace('.', '').replace(':00 ', '')
        courts[hour] = {'booked': [], 'free': []}

        table_data = tr.find_all('td', {'class': 'table-data'})
        for idx, td in enumerate(table_data):
            if td.get_text(strip=True):
                courts[hour]['booked'].append(str(idx + 13))
            else:
                courts[hour]['free'].append(str(idx + 13))
    return courts


if __name__ == '__main__':
    courts = get_courts('06-Oct-2024')
    print(courts)
