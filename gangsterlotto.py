#this script is for running the lottery on my pixel gangsters collection! feel free to change and use as needed. 
#you're all wonderful humans. -kerkus_

import random
import numpy as np
import json
import requests
import time
import calendar
import datetime


#this returns the sales in my collection (collection name 424521244421 - pixel gangsters)
strget = "https://proton.api.atomicassets.io/atomicmarket/v1/sales?state=3&collection_whitelist=424521244421&page=1&limit=100&order=desc&sort=created"

#this script is for running the lottery on my pixel gangsters collection! feel free to change and use as needed. (please give credit ^^)
r = requests.get(strget)

totalsales = json.loads(r.content.decode())

#week ago in epoch time
current_time = datetime.datetime.fromtimestamp(time.time()) 

#iterate 
sales = 0
resales = 0
for i in range(len(totalsales["data"])):
    time_updated = int(totalsales["data"][i]["assets"][0]["updated_at_time"])/1000 #account for ms
    time_updated = datetime.datetime.fromtimestamp((time_updated))

    if not (((current_time)-(time_updated)).days>7):
        if (totalsales["data"][i]['seller']) == 'kerkus' and totalsales["data"][i]["assets"][0]['prices'][0]['sales'] == '1':
            sales += int(totalsales["data"][i]['price']['amount'])/1000000
        if (totalsales["data"][i]['seller']) != 'kerkus':
            resales += int(totalsales["data"][i]['price']['amount'])/1000000

#this is the value that the pot gets. 30 percent of sales and 20 percent of resales.
pot = sales*.30 + resales*0.08*0.2

#rarities next: my collection adheres to the following structure: common x3, uncommon, common x3, uncommon, common x3, rare, badge. a badge gives no tickets. common gives 2, uncommon 3, rare 4. legendaries are left out for now. (will give 8)
#we'll be using the assets list from the api in ascending order to determine both holders and rarity:

reqstr = "https://proton.api.atomicassets.io/atomicassets/v1/assets?collection_name=424521244421&page=1&limit=500&order=asc&sort=asset_id"
r2 = requests.get(reqstr)
holders_rarity = json.loads(r2.content.decode())

#this is ugly code but it is EASY code.
ownerlist = []
uncommon = 4
rare = 12
badge = 13
count = 0

#iterate over the assets + holders, add their names to the list with weights for rarity 
for i in range((len(holders_rarity['data']))):
    count += 1
    if count == uncommon or count == uncommon * 2:
        ownerlist.extend([holders_rarity["data"][i]["owner"]]*2)
    if count == rare:
        ownerlist.extend([holders_rarity["data"][i]["owner"]]*4)
    if count != uncommon and count != uncommon*2 and count != rare and count != badge:
        ownerlist.append(holders_rarity["data"][i]["owner"])
    if count == badge:
        count = 0


#this operation happens in place, shuffle the list for fair random pick.
random.shuffle(ownerlist)

print("Winner of the pot worth $" + str(pot) + " is: " + random.choice(ownerlist))
