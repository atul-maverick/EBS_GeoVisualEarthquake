from flask import Flask, render_template
from urllib.request import urlopen
import csv
import json

application = Flask(__name__)


@application.route('/')
def hello_world():
    return render_template('default.html')


def parse_process_csv(fileopen):
    reader = csv.reader(fileopen)
    # print fieldnames
    fileopen=[line.decode(encoding='UTF-8') for line in fileopen]
    fn=fileopen[0].split(',')
    data_dict = csv.DictReader(fileopen[1:], fieldnames=fn)
    final_value = []
    # final_value.append(['Lat', 'Long', 'Name','mag'])
    i = 0
    for row in data_dict:
        i = i + 1
        if (row['latitude'] == "FALSE" or row['longitude'] == "FALSE" or row['mag'] == ""):
            continue
            # print(row['latitude'],row['longitude'])
        try:
            final_value.append(
                [float(row['latitude']), float(row['longitude']), "Place:" + row['place'] + "  Time: " + row['time'],
                 float(row['mag'])])
        except ValueError:
            print(row['latitude'], row['longitude'], row['mag'])
    return final_value


@application.route('/getData/<duration>')
def process(duration):
    url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv'
    inpfile = urlopen(url)
    # inpfile=open("all_month.csv",'rb')
    final_value = parse_process_csv(inpfile)
    # print(final_value)
    return json.dumps(final_value)


if __name__ == '__main__':
    application.debug = True
    application.run()
