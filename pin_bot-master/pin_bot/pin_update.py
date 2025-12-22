#!/usr/bin/env python3

from bot import telegram_chatbot
import yaml
import time
import json
import sys
import subprocess as sp

if len(sys.argv) <= 3 or len(sys.argv) >= 5:
  print("/pin/pin_check.py [message_id] [chat_id]")
  sys.exit()

message_id_1 = str(sys.argv[1])
message_id_2 = str(sys.argv[2])
chat_id = str(sys.argv[3])

with open("config.yaml", "r") as config:
  cfg = yaml.safe_load(config)

bot = telegram_chatbot(cfg['bot_id'])

msg_1 = sp.check_output("./domain_template_1.py")
msg_2 = sp.check_output("./domain_template_2.py")

#edit_message(msg, chat_id, message_id)
bot.edit_message(msg_1.decode(), chat_id, message_id_1)
bot.edit_message(msg_2.decode(), chat_id, message_id_2)