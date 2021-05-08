import requests
import json
import configparser as cfg
import time
from datetime import datetime
today_date = datetime.today().strftime('%d-%m-%Y')
print (today_date)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'}


class telegram_chatbot():
    def read_token_from_config_file(self, config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', 'token')
    def __init__(self):
        self.token = self.read_token_from_config_file("config.cfg")
        self.base = "https://api.telegram.org/bot{}/".format(self.token)
    
    def get_updates():
        url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=390&date="+today_date
        r = requests.get(url,headers=headers)
        return json.loads(r.content)

    def send_message(self, msg):
        #https://api.telegram.org/bot1821372590:AAFDq0mYH1a8SvA9Z7r-K_PoU15EBVOlgT4/sendMessage?chat_id=@jalgaon18&text=Hi
        url = self.base + "sendMessage?chat_id=@jalgaon45&text={}".format(msg)
        if msg is not None:
            requests.get(url,headers=headers)
previous_results = {}
while True:
    results = telegram_chatbot.get_updates()
    print ("fetched")
    doNotSendNewMsg = (sorted(results.items()) == sorted(previous_results.items()))
    if(doNotSendNewMsg == False):
        for center in results['centers']:
            for session in center['sessions']:
                if(session['min_age_limit'] == 45 and session['available_capacity'] > 0):
                    slotsAvailableMsg = "Age Group: 45 and above \nCenter Name:"+center['name']+"\nPin Code:"+str(center['pincode'])+"\nDate:"+session['date']+"\nAvailable Capacity:"+str(session['available_capacity'])+"\nFee Type:"+center['fee_type']+"\nVaccine:"+session['vaccine']+"\n\nhttps://selfregistration.cowin.gov.in/"
                    print (slotsAvailableMsg)
                    telegram_chatbot().send_message(slotsAvailableMsg)
    time.sleep(3)
    previous_results = results