import json
import datetime, calendar, time
import pymongo
import requests

token_url = "https://eu.battle.net/oauth/token"

#client (application) credentials on apim.byu.edu
client_id = ''
client_secret = ''

#step A, B - single call with client credentials as the basic auth header - will return access_token
data = {'grant_type': 'client_credentials'}

access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))

print(access_token_response.headers)
print(access_token_response.text)

tokens = json.loads(access_token_response.text)

print ("access token: " + tokens['access_token'])

url = "https://eu.api.blizzard.com/data/wow/connected-realm/1390/auctions"
payload  = {'access_token': tokens['access_token'], 'locale': 'fr_FR', 'namespace': 'dynamic-eu'}
testReal = requests.get(url, params = payload).content

gmt = time.gmtime()
ts = calendar.timegm(gmt)
timestamp = str(ts)

#testReal='{"_links":{"self":{"href":"https://eu.api.blizzard.com/data/wow/connected-realm/1390/auctions?namespace=dynamic-eu"}},"connected_realm":{"href":"https://eu.api.blizzard.com/data/wow/connected-realm/1390?namespace=dynamic-eu"},"auctions":[{"id":942650037,"item":{"id":171292},"quantity":32,"unit_price":458600,"time_left":"SHORT"},{"id":942650043,"item":{"id":172234,"context":13,"bonus_lists":[6890],"modifiers":[{"type":9,"value":60},{"type":28,"value":391},{"type":29,"value":36},{"type":30,"value":40}]},"buyout":936300,"quantity":1,"time_left":"SHORT"},{"id":942650044,"item":{"id":172234,"context":13,"bonus_lists":[6890],"modifiers":[{"type":9,"value":60},{"type":28,"value":391},{"type":29,"value":32},{"type":30,"value":49}]},"buyout":936300,"quantity":1,"time_left":"SHORT"}]}'
testobjReal=json.loads(testReal)
testobjReal=testobjReal['auctions']

myclient = pymongo.MongoClient("mongodb://admin:root@mongodb:27017")
mydb = myclient["audot"]
mycol = mydb["auction_items"]

for f in testobjReal:
    iteminfo=f['item']
    f['date']=timestamp
    f.pop('item',None)
    f.pop('id',None)
    f.pop('bid',None)
    f['id_item']=iteminfo['id']

mydict = testobjReal
x = mycol.insert_many(mydict)

print(type(testobjReal))
