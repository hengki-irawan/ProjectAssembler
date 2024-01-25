#!/usr/bin/env python3
import http.client
import json
import csv
import configparser


#read config
config = configparser.ConfigParser()
config.read('/Users/hengki.irawan/Documents/Coding practice/CH/config.cfg')
def main():
      #getting data from API
      connection = http.client.HTTPConnection('api.football-data.org')
      headers = {'X-Auth-Token':  config.get('TOKEN','auth_token')}
      connection.request('GET', '/v2/competitions/PL', None, headers )
      response = json.loads(connection.getresponse().read().decode())
      # print(response)
      
      #download data in csv and store it in local machine
      raw_data = response['seasons']

      with open('pl_raw.csv', 'w') as f:
            csvwriter = csv.writer(f)
            count = 0
            for d in raw_data:
                  if count == 0:
                        header = d.keys()
                        csvwriter.writerow(header)
                        count += 1
                  csvwriter.writerow(d.values())
            f.close()

main()