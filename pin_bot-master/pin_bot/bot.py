#!/usr/bin/env python3

import requests
import json
import configparser as cfg
import yaml
import urllib.parse

class telegram_chatbot():
    def __init__(self, config):
        self.token = self.read_token_from_config_file(config)
        self.base = "https://api.telegram.org/bot{}/".format(self.token)

    def get_updates(self, offset=None):
        url = self.base + "getUpdates?timeout=100"
        if offset:
            url += "&offset={}".format(offset + 1)
        r = requests.get(url)
        return json.loads(r.content)

    def send_message(self, msg, chat_id):
        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        if msg is not None:
            requests.get(url)

    def edit_message(self, msg, chat_id, message_id):
        url_msg = urllib.parse.quote_plus(msg)
        url = self.base + "editMessageText?message_id={}&chat_id={}&text={}".format(message_id, chat_id, url_msg)
        requests.get(url)

    def pin_message(self, chat_id, message_id):
        url = self.base + "pinChatMessage?message_id={}&chat_id={}".format(message_id, chat_id)
        print(url)
        requests.get(url)

    def read_token_from_config_file(self, config):
        return config 
