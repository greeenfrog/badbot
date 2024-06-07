import requests
import time

import bnh
import config

graph_url = 'https://graph.facebook.com/v20.0/'
conversations = {}


def get_conversations():
    url = f'{graph_url}{config.page_id}/conversations'
    params = {
        'platform': 'instagram',
        'access_token': config.page_access_token,
    }
    r = requests.get(url, params)
    return r.json()['data']


def get_msgs(conversation_id):
    url = f'{graph_url}{conversation_id}'
    params = {
        'fields': 'messages',
        'access_token': config.page_access_token,
    }
    r = requests.get(url, params)
    return r.json()['messages']['data']


def view_msg(msg_id):
    url = f'{graph_url}{msg_id}'
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
    ret_msg = bnh.get_ret(msg)
    print(send_msg(igsid, ret_msg))
    print()


def send_msg(igsid, msg):
    url = f'{graph_url}me/messages'
    params = {'access_token': config.page_access_token}
    data = {
        'recipient': {'id': igsid},
        'message': {'text': msg},
    }
    r = requests.post(url, params=params, json=data)
    return r.json()


def run():
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
    run()
