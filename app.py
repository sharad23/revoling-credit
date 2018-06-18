from flask import Flask, render_template, request, send_from_directory
from lib.execute import daily_reporting, transaction_reporting
import json
import csv

PATH = '~/revolving_cr/'
DOMAIN = 'http://localhost:5000/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PATH


@app.route('/', methods=['GET'])
def dashboard():
   return render_template('home.html', domain=DOMAIN)


@app.route('/daily-reporting', methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        filename, ext = f.filename.split('.')
        filename = filename + '_'
        print('here')
        print(filename, ext)
        with open(f.filename) as json_data:
            daily = json.load(json_data)
            results = daily_reporting(**daily)
            if results:
                keys = results[0].keys()
                with open(filename+'.csv', 'w') as csv_file:
                    c = csv.writer(csv_file)
                    c.writerow(keys)
                    for result in results:
                        c.writerow(result.values())
        # return 'complete'
        return send_from_directory(directory='.', filename=filename+'.csv')

    else:
        return render_template('daily.html', domain=DOMAIN)
    # return 'Hello World'


@app.route('/trans-reporting', methods=['POST', 'GET'])
def hello2():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        filename, ext = f.filename.split('.')
        filename = filename + '_'
        print('here')
        print(filename, ext)
        with open(f.filename) as json_data:
            trans = json.load(json_data)
            results = transaction_reporting(**trans)
            if results:
                keys = results[0].keys()
                with open(filename+'.csv', 'w') as csv_file:
                    c = csv.writer(csv_file)
                    c.writerow(keys)
                    for result in results:
                        c.writerow(result.values())

        return send_from_directory(directory='.', filename=filename + '.csv')
        # return 'complete'

    else:
        return render_template('trans.html', domain=DOMAIN)
    # return 'Hello World'


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)