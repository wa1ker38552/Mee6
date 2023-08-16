from threading import Thread
from flask import Flask
import datetime
import requests
import random
import time

class Client:
  def __init__(self, token, configs):
    self.token = token
    self.__client = requests.Session()
    self.__client.headers = {'Authorization': self.token}
    self.client_data = self.__client.get('https://discord.com/api/v9/users/@me').json()
    self.configs = configs

  def send_message(self, content, channel):
    self.__client.post(f'https://discord.com/api/v9/channels/{channel}/messages',
                       json={'content': content})

  def run_flask(self, host, port):
    self.app = Flask(__name__)

    @self.app.route('/')
    def index():
      return '<script>window.onload = function() {setInterval(async function() {const a = await fetch("/")}, 30000)}</script>'

    Thread(target=lambda: self.app.run(host, port)).start()

  def run(self, economy_channel, counting_channel):
    print(f'[DEBUG] Running on: {self.client_data["username"]}')
    Thread(target=lambda: self.run_economy(economy_channel)).start()
    Thread(target=lambda: self.run_counting(counting_channel)).start()

  def run_economy(self, channel):
    print('[DEBUG] Running economy')
    msg_min, msg_max = self.configs.economy.messages_variation[0], self.configs.economy.messages_variation[1]
    int_min, int_max = self.configs.economy.interval_variation[0], self.configs.economy.interval_variation[1]
    hrs_min, hrs_max = self.configs.hours.hours_variation[0], self.configs.hours.hours_variation[1]
    hours = self.configs.hours.hours
    while True:
      cur_hour = datetime.datetime.now().hour
      if cur_hour in hours:
        if cur_hour == hours[0] or cur_hour == hours[len(hours)-1]:
          time.sleep(random.randint(hrs_min, hrs_max))
 
        for message in self.configs.economy.messages:
          self.send_message(message, channel)
          time.sleep(random.randint(msg_min, msg_max))
        time.sleep(self.configs.economy.interval)
        time.sleep(random.randint(int_min, int_max))
      else:
        time.sleep(30)

  def run_counting(self, channel):
    print('[DEBUG] Running counting')
    cnt_min, cnt_max = self.configs.counting.interval_variation[0], self.configs.counting.interval_variation[1]
    hrs_min, hrs_max = self.configs.hours.hours_variation[0], self.configs.hours.hours_variation[1]
    hours = self.configs.hours.hours
    while True:
      cur_hour = datetime.datetime.now().hour
      if cur_hour in hours:
        if cur_hour == hours[0] or cur_hour == hours[len(hours)-1]:
          time.sleep(random.randint(hrs_min, hrs_max))

        if random.randint(0, 100) <= self.configs.counting.probability*100:
          last_message = self.__client.get(f'https://discord.com/api/v9/channels/{channel}/messages').json()[0]
          if str(last_message['author']['id']) != str(self.client_data['id']):
            try:
              count = int(last_message['content'])+1
              self.send_message(count, channel)
              print(f'[DEBUG] Added {count} to the count')
            except ValueError:
              pass
        interval = self.configs.counting.interval+random.randint(cnt_min, cnt_max)
        time.sleep(interval)
      else:
        time.sleep(30)
