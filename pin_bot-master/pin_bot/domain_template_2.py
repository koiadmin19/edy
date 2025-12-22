#!/usr/bin/env python3
import yaml
import requests
import re
import json
import time
import subprocess as sp

domain_group = ['baoyu', 'meigui', 'nvwang', 'gongzhu']
domain_landing = ['mg_landing', 'by_landing', 'nv_landing', 'gz_landing']
domain_main = ['mg_main', 'by_main', 'nv_main', 'gz_main']
master_pin = ['google chrome access test']
check_time = {
                'Main Domain':'every 4H',
                'Events Domain':'every 4h',
                'Domains':'every 1h',
                'APK TEST':'every 30m'
             }
with open("domains.yaml", "r") as domain_file:
  domain_list = yaml.safe_load(domain_file)

with open("domains.yaml_shadow", "r") as domain_file:
  domain_list_shadow = yaml.safe_load(domain_file)

with open("config.yaml", "r") as configs:
  conf = yaml.safe_load(configs)

with open("cnzz.yaml", "r") as c_cnf:
  cnzz_conf = yaml.safe_load(c_cnf)

with open("afeng.yaml", "r") as a_cnf:
  afeng_conf = yaml.safe_load(a_cnf)

loki_url = conf["loki"]["url"] + conf["loki"]["api"]
mg_job = conf["loki"]["mg_job"]
gz_job = conf["loki"]["gz_job"]
is_loki = conf["loki"]["enabled"]
counter = conf["counter"]
cnzz_group = cnzz_conf["cnzz"]
la51_group = cnzz_conf["51la"]
afeng_group = afeng_conf["afeng"]

def get_domain_val(domain, channel, job):
  try:
    #logql_query = 'count_over_time({{job="{}"}} |= `GET /?channelCode={} ` |= `{}` [1h])'.format(job, channel, domain)
    #logql_query = 'count_over_time({{job="{}"}} |~ `GET \/\?channelCode\={}\*?[0-9]?[0-9]?[0-9]?[0-9]? ` |= `{}` [1h])'.format(job, channel, domain)
    logql_query = 'count_over_time({{job="{}"}} |~ `GET \/\?channelCode\={}\*?[0-9]?[0-9]?[0-9]?[0-9]? ` |~ `{}[^0-9]` |= `{}` [1h])'.format(job, channel, channel, domain)
    payload = {'query':logql_query}
    req = requests.get(loki_url, params=payload)
    time.sleep(0.1)
    json_data = json.loads(req.text)
    to_return = json_data['data']['result'][0]['value'][1]
  except Exception as error:
    to_return = None
  return to_return
  
def get_channel_val(channel, job, domains):
  try:
    #logql_query = 'count_over_time({{job="{}"}} |= `GET /?channelCode={} ` != `touliang` != `{}` [1h])'.format(job, channel, domains)
    #logql_query = 'count_over_time({{job="{}"}} |~ `GET \/\?channelCode\={}\*?[0-9]?[0-9]?[0-9]?[0-9]? ` != `touliang` != `{}` [1h])'.format(job, channel, domains)
    logql_query = 'count_over_time({{job="{}"}} |~ `GET \/\?channelCode\={}\*?[0-9]?[0-9]?[0-9]?[0-9]? ` |~ `{}[^0-9]` != `touliang` != `{}` [1h])'.format(job, channel, channel, domains)
    payload = {'query':logql_query}
    req = requests.get(loki_url, params=payload)
    time.sleep(0.1)
    json_data = json.loads(req.text)
    to_return = json_data['data']['result'][0]['value'][1]
  except Exception as error:
    to_return = None
  return to_return
  
#def get_channel_val(channel):


for group in domain_list:
  if group not in master_pin:
    continue
  print('---------------------------------')
  print(group)
  try:
    print(check_time[group])
  except:
    pass
  print('---------------------------------')
  for domains in domain_list[group]:
    if domains in domain_landing:
      for landing in domain_list[group][domains]:
        print("------> {}".format(landing))
      print("")
      continue
    if domains in domain_main:
      print(domain_list[group][domains])
      continue
    if domains in domain_group:
      print("")
      print("--- {}".format(domains))
      for channel in domain_list[group][domains]:
        is_cnzz = False 
        is_afeng = False
        is_la51 = False
        domain = re.search(r"[a-zA-Z0-9]+\.[a-zA-Z]+", channel).group()
        channel_code = re.search(r"[a-zA-Z]+\_[0-9]+", channel).group()
        if channel_code in cnzz_group:
          is_cnzz = True
        if channel_code in afeng_group:
          is_afeng = True
        if channel_code in la51_group:
          is_la51 = True
        if domains != 'gongzhu':
          domain_count = get_domain_val(domain, channel_code, mg_job)
          channel_count = get_channel_val(channel_code, mg_job, domains)
        else:
          domain_count = get_domain_val(domain, channel_code, gz_job)
          channel_count = get_channel_val(channel_code, gz_job, domains)
        if channel_count is None:
          channel_count = 0
        if domain_count is None:
          domain_count = 0
        if int(channel_count) >= int(counter) or channel not in domain_list_shadow[group][domains]:
          try:
            percent_value = sp.check_output(['bash', 'percent.sh', channel_code ]).decode("UTF-8")
          except:
            percent_value = "error"
          to_send = "{}  [{}/{}] [{}]".format(channel, domain_count, channel_count,percent_value.strip())
          if is_la51:
            to_send = "{} **51LA**".format(to_send)
          if is_cnzz:
            to_send = "{} **CNZZ**".format(to_send)
          if is_afeng:
            to_send = "**AFENG**{}".format(to_send)
          print(to_send)
#          if is_cnzz:
#            print("**CNZZ**{}  [{}/{}] [{}]".format(channel, domain_count, channel_count,percent_value.strip()))
#          elif is_afeng:
#            print("**AFENG**{}  [{}/{}] [{}]".format(channel, domain_count, channel_count,percent_value.strip()))
#          else:
#            print("{}  [{}/{}] [{}]".format(channel, domain_count, channel_count,percent_value.strip()))
    else:
      print(domains)
      print("")