import requests
import sys
import argparse
import csv
import json




def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', default='config.json')
    return parser

parser = createParser()
namespace = parser.parse_args (sys.argv[1:])


with open(namespace.config) as config_file:
    config = json.load(config_file)


f = open(config['log_file'], 'w')
with open(config['read_data'], newline='') as csvfile:
    data = csv.reader(csvfile)
    i = 1
    for row in data:
        comm = 'http://{}:{}@{}/ISAPI/System/externalDevice/supplementLight'.format(row[1], row[2], row[0])
        r = requests.get(comm)
        if r.status_code == 200:

            payload = """<?xml version="1.0" encoding="UTF-8"?>
<ExternalDevice version="2.0"
xmlns="http://www.hikvision.com/ver20/XMLSchema">
<SupplementLight>
<enabled>true</enabled>
<mode>{}</mode>
<Schedule>
<TimeRange>
<beginTime>{}</beginTime>
<endTime>{}</endTime>
</TimeRange>
</Schedule>
<lowBeamBrightness>{}</lowBeamBrightness>
<highBeamBrightness>{}</highBeamBrightness>
</SupplementLight>
</ExternalDevice>""".format(config['mode'], config['beginTime'], config['endTime'],
                            config['lowBeamBrightness'], config['highBeamBrightness'])
            re = requests.put(comm, data=payload)
            if re.status_code == 200:
                print("row ", i, " updated.")
                f.write("row {} updated, ip : {} \n".format(i, row[0]))
            else:
                print("error in XML data.")
                f.write("error in XML data, row : {}, ip :  {} \n".format(i,row[0]))
        else:
            print("wrong ip/login/psw, row : ", i)
            f.write("row : {}, wrong ip/login/psw, ip : {} \n".format(i,row[0]))
        i += 1