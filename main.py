from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

global username, fed
username = ""
fed = 0


@app.route('/')
def homepage():
    global username, fed
    if username == "":
        username = "Rishit"
        fed = 2000
    if username.lower() != "rishit":
        fed = 0
    if username.lower() == "rishit":
        fed = 2000
    return render_template('index.html', user=username, fed=fed)


@app.route('/connect', methods=['POST', 'GET'])
def connect_page():
    global username

    login = bool
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        with open('static/data/userdata.csv', mode="r") as f1:
            data = f1.readlines()
            for row in data:
                name, pas = row.split(',')
                pas = pas.strip()
                if username == name:
                    if password == pas:
                        login = True
                        return redirect('/join')
                    else:
                        login = False
                else:
                    login = False
    return render_template('connect.html', login=login)


@app.route('/register', methods=['POST', 'GET'])
def register():
    msg = False
    global username

    if request.method == "POST":
        msg = True
        username = request.form['username']
        password = request.form['password']
        insert_data = '\n' + str(username) + ',' + str(password)
        with open('static/data/userdata.csv', mode="a") as f:
            f.write(insert_data)
        return render_template('register.html', msg=msg)

    return render_template('register.html', msg=msg)


@app.route('/join')
def join():
    return render_template('join.html')


@app.route('/work')
def work():
    return render_template("work.html")


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    msg = False
    if request.method == "POST":
        msg = True
        url = "https://discord.com/api/webhooks/1160539846738186240/QMlwfKJodJmBfmVYtlkOAn07iO1eRT5JHlw9xFHLYrsR7gE2tX2Mq46ooB-yh4pqUHCZ"
        data = {
            "username": request.form['username']
        }
        data["embeds"] = [
            {
                "description": request.form['contact'],
                "title": request.form['username']
            }
        ]
        result = requests.post(url, json=data)

        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        return render_template('contact.html', msg=msg)

    return render_template('contact.html', msg=msg)


if __name__ == '__main__':
    app.run(debug=True)
