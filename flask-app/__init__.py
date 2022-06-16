import calendar
from flask import Flask, render_template, request, send_file, Response, url_for
import requests
import boto3
from boto3 import client
from boto3.session import Session
from datetime import datetime
import botocore
from werkzeug.utils import redirect

app = Flask(__name__)

key_id = "AKIA2QP575JUM2YECDAT"
secret_access_key = "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"
bucket_name = "bucket.for.html.hosting"

# client_s3 = boto3.client(
#     's3',
#     aws_access_key_id=key_id,
#     aws_secret_access_key=secret_access_key
# )

BUCKET_NAME = 'bucket.for.html.hosting'  # replace with your bucket name
KEY = '1.jpg'  # replace with your object key
s3 = boto3.resource('s3')


def get_client():
    return client(
        's3',
        'us-east-1',
        aws_access_key_id='AKIA2QP575JUM2YECDAT',
        aws_secret_access_key='woK8tP/iPwOeXtyoPdrYcgLc+AgOITyX0Fh+Bgdl'
    )


city = ''
concurrent_temp = ''


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if all(x.isalpha() or x.isspace() for x in request.form['search']):
            try:
                location = request.form['search']
                construct_url = "http://api.openweathermap.org/data/2.5/forecast?q=" + location + "&appid=762846685b807dc35c6c4e27ffe0cfb8"

                response = requests.get(construct_url)
                list_of_data = response.json()
                lat = str(list_of_data['city']['coord']['lat'])
                lon = str(list_of_data['city']['coord']['lon'])
                country = str(list_of_data['city']['country'])
                global city
                city = str(list_of_data['city']['name'])
                construct_url2 = 'https://api.openweathermap.org/data/2.5/onecall?lat=' + lat + '&lon=' + lon + '&units=metric&exclude=minutely,hourly,alerts&appid=8742a3dfbd48914e2ae78621ab123a83&cnt=7'
                response2 = requests.get(construct_url2)
                list_of_data2 = response2.json()

                list_of_days = []
                list_of_dates = []
                list_of_temp_average = []
                list_of_temp_morning = []
                list_of_temp_evening = []
                list_of_humidity = []
                list_of_icons = []
                list_of_icons_night = []
                list_of_description = []
                global concurrent_temp
                concurrent_temp = str(round(list_of_data2['current']['temp']))
                for i in range(0, 8):
                    ts = int(str(list_of_data2['daily'][i]['dt']))
                    dat = datetime.utcfromtimestamp(ts).strftime('%d-%m-%Y')
                    list_of_dates.append(str(dat))
                    date_by_date = datetime.strptime(dat, '%d-%m-%Y').weekday()
                    day_date = calendar.day_name[date_by_date]
                    list_of_days.append(str(day_date))
                    list_of_temp_average.append(str(round(list_of_data2['daily'][i]['temp']['day'])))
                    list_of_temp_morning.append(str(round(list_of_data2['daily'][i]['temp']['day'])))
                    list_of_temp_evening.append(str(round(list_of_data2['daily'][i]['temp']['night'])))
                    list_of_humidity.append(str(list_of_data2['daily'][i]['humidity']))
                    list_of_icons.append(str(list_of_data2['daily'][i]['weather'][0]['icon']))
                    list_of_icons_night.append(str(list_of_data2['daily'][i]['weather'][0]['icon']))
                    list_of_description.append(str(list_of_data2['daily'][i]['weather'][0]['description']))

                print(list_of_data2)
                print(datetime.now())
                return render_template('index.html', country=country, city=city,
                                       list_of_data2=list_of_data2, list_of_days=list_of_days,
                                       list_of_temp_average=list_of_temp_average,
                                       list_of_temp_evening=list_of_temp_evening,
                                       list_of_temp_morning=list_of_temp_morning, concurrent_temp=concurrent_temp,
                                       list_of_humidity=list_of_humidity, list_of_dates=list_of_dates,
                                       list_of_icons=list_of_icons, list_of_description=list_of_description)
            except KeyError:
                return render_template('city.html')
    return render_template('welcome.html')


@app.route('/download', methods=['GET'])
def download_file():
    s3 = get_client()
    file = s3.get_object(Bucket='bucket.for.html.hosting', Key='1.jpg')
    return Response(
        file['Body'].read(),
        mimetype='image/jpg',
        headers={"Content-Disposition": "attachment;filename=test_sky.jpg"}
    )


@app.route('/upload', methods=['GET', 'POST'])
def upload_file_to_dynamodb():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Temperature_Data')
    global city
    global concurrent_temp
    table.put_item(
        Item={
            'ID': str(datetime.timestamp(datetime.now())),
            'city': str(city),
            'Temp': str(concurrent_temp),
            'Date': str(datetime.now().strftime("%Y-%m-%d")),

        }
    )
    return Response()


if __name__ == '__main__':
    app.run(debug=True)
