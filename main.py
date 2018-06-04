# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import json
import urllib2
import jinja2
from html import HTML

import tweepy

plants = {}

# TWEET POSTING FUNCTIONS
def get_api(cfg):
  auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
  auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
  return tweepy.API(auth)

def post_tweet(text):
  cfg = { 
    "consumer_key"        : "rxuE1QrNtDkg1uR8MQu3PvUhj",
    "consumer_secret"     : "SSmIG2Dp2fAawrmW0gJoGuXNCc4tNQt1QOyoTakaZQqrtrdhP0",
    "access_token"        : "1002700485277540352-FZDAwumhugRLTdON3VPTHzMOKCH65q",
    "access_token_secret" : "FsDNNUdMxuFS4wxOmiTkg6k7oo7JRAYAKkwG4zTe0ryGD" 
    }
  api = get_api(cfg)
  tweet = text
  status = api.update_status(status=text) 


class Plant:

    def __init__(self, identifier):
        self.identifier = identifier
        self.name =  "unknown"
        self.species = "unknown"
        self.current = 0
        self.waterHist = []
        self.statusHist = []

    def updateWaterHist(self, value):
        self.waterHist.append(value)

    def updateStatusHist(self, value):
        self.statusHist.append(value)

    def updateCurrentStatus(self, value):
        self.current = value

    def updateInfo(self, name):
        self.name = name
        

def generate_table():
    
    h = HTML()
    htmlcode = h.table(border='1')

    r = htmlcode.tr
    r.td('Identifier')
    r.td('Name')
    r.td('Current Status')
 #   r.td('Status')

    for plant in plants:
        info = plants[plant]
        r = htmlcode.tr
        r.td(str(plant))
        r.td(str(info.name))
        r.td(str(info.current))

        if (str(info.name) == "unknown"):
            r.td("button")

    return htmlcode
    


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/html"
        self.response.write("""
          <html>
            <head><title>iPlant</title></head>
            <body>
            <form action="/test" method="get">
            <button name="subject" type="submit" value="temp">Temp Converter</button>
            </form>
            </body>
          </html>""")

        self.response.write(generate_table())
        
   #     self.response.headers['Content-Type'] = 'text/plain'
#        self.response.write('Hello, World!')
        
    def post(self):
    	myjson = json.loads(self.request.body)
    	self.response.headers['Content-Type'] = 'text/plain'
    	self.response.write(myjson)

    	plantId = myjson["id"]
    	newData = myjson["data"]
        print("*********")
        #print(myjson)

        if plantId in plants:
            plants[plantId].updateStatusHist(newData)
            plants[plantId].updateCurrentStatus(newData)
        else:
            print("error")
                
    	print("plant contents: ")
    	print(plants)
    	#post_tweet()

class NewPlant(webapp2.RequestHandler):
    def post(self):
        myjson = json.loads(self.request.body)
        self.response.headers['Content-Type'] = 'text/plain'
	self.response.write(myjson)

	plantId = myjson["id"]

        #creates new plant object for dictionary
	plants[plantId] = Plant(plantId)


def convert_temp(cel_temp):
    ''' convert Celsius temperature to Fahrenheit temperature '''
    if cel_temp == "":
        return ""
    try:
        far_temp = float(cel_temp) * 9 / 5 + 32
        far_temp = round(far_temp, 3)  # round to three decimal places
        return str(far_temp)
    except ValueError:  # user entered non-numeric temperature
        return "invalid input"


class TestPage(webapp2.RequestHandler):
    def get(self):
        cel_temp = self.request.get("cel_temp")
        far_temp = convert_temp(cel_temp)
        self.response.headers["Content-Type"] = "text/html"
        self.response.write("""
          <html>
            <head><title>Temperature Converter</title></head>
            <body>
            <form action="/" method="get">
            <button name="subject" type="submit" value="back">Go back</button>
            </form>
            
              <form action="/test" method="get">
                Celsius temperature: <input type="text"
                                        name="cel_temp" value={}>
                <input type="submit" value="Convert"><br>
                Fahrenheit temperature: {}
              </form>
            </body>
          </html>""".format(cel_temp, far_temp))       


routes = [
    ('/', MainPage),
    ('/new', NewPlant),
    ('/test', TestPage)
    #(r'/recv/(\d+)', RecvData)
]

app = webapp2.WSGIApplication(routes, debug=True)

def main():
    from paste import httpserver
    httpserver.serve(app, host='127.0.0.1', port='8080')

if __name__ == '__main__':
    main()
