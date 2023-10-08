from flask import Flask, render_template, request, redirect

app = Flask(__name__)

global username
username = ""


@app.route('/')
def homepage():
    global username
    if username == "":
        username = "Rishit"
    return render_template('index.html', user=username)


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


if __name__ == '__main__':
    app.run(debug=True)
