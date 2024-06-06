import datetime as dt
import requests
import time

from bnh import get_courts
import config

fb_url = 'https://graph.facebook.com/v20.0/'
conversations = {}


def get_conversations():
    url = f'{fb_url}{config.page_id}/conversations'
    params = {
        'platform': 'instagram',
        'access_token': config.page_access_token,
    }
    r = requests.get(url, params)
    return r.json()['data']


def get_msgs(conversation_id):
    url = f'{fb_url}{conversation_id}'
    params = {
        'fields': 'messages',
        'access_token': config.page_access_token,
    }
    r = requests.get(url, params)
    return r.json()['messages']['data']


def view_msg(msg_id):
    url = f'{fb_url}{msg_id}'
    params = {
        'fields': 'id,created_time,from,to,message',
        'access_token': config.page_access_token,
    }
    r = requests.get(url, params)
    return r.json()


def process_request(conversation_id):
    msg_id = get_msgs(conversation_id)[0]['id']
    msg_data = view_msg(msg_id)
    print(msg_data)
    print()

    igsid = msg_data['from']['id']
    if igsid == config.igsid:
        return
    msg = msg_data['message'].strip().lower()

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

    print(send_msg(igsid, ret_msg))
    print()

def send_msg(igsid, msg):
    url = f'{fb_url}me/messages'
    params = {'access_token': config.page_access_token}
    data = {
        'recipient': {'id': igsid},
        'message': {'text': msg},
    }
    r = requests.post(url, params=params, json=data)
    return r.json()


def main():
    while True:
        for c in get_conversations():
            conversation_id = c['id']
            updated_time = c['updated_time']
            if conversation_id in conversations:
                if updated_time != conversations[conversation_id]:
                    process_request(conversation_id)
                    conversations[conversation_id] = updated_time
            else:
                process_request(conversation_id)
                conversations[conversation_id] = updated_time
        time.sleep(0.1)


if __name__ == '__main__':
    main()
