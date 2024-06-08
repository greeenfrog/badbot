import datetime as dt
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


def get_ret(msg):
    msg = msg.strip().lower()
    date = None
    if msg in ['now', 'today', 'tdy']:
        date = dt.date.today()
    elif msg in ['tomorrow', 'tmr']:
        date = dt.date.today() + dt.timedelta(days=1)
    elif len(msg) == 6 and msg.isdigit():
        date = dt.datetime.strptime(msg, '%d%m%y').date()

    if date:
        date_string = date.strftime('%d-%b-%Y')
        courts = get_courts(date_string)
        if courts:
            ret = [f'{date_string}@Apollo']
            for hour, status in courts.items():
                if not status['booked']:
                    hour += ' EMPTY'
                elif not status['free']:
                    hour += ' FULL'
                else:
                    hour += f"\nBooked: {', '.join(status['booked'])}"
                    hour += f"\nFree: {', '.join(status['free'])}"
                ret.append(hour)
            ret_msg = '\n\n'.join(ret)
        else:
            ret_msg = f'No info for date: {msg}'
    else:
        ret_msg = (
            'Hi! I am a bad bot.\n\n'
            '"now", "today" or "tdy" for court info today\n\n'
            '"tomorrow" or "tmr" for court info tomorrow\n\n'
            '"ddmmyy" for other dates')

    return ret_msg


if __name__ == '__main__':
    print(get_ret('now'))
    print()
    print(get_ret('tmr'))
    print()
    print(get_ret('070724'))
