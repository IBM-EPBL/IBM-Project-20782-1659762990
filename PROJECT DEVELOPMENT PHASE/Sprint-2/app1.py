from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re

app = Flask(__name__)
  
app.secret_key = 'a'

conn = ibm_db.connect('DATABASE=bludb;HOSTNAME=2d46b6b4-cbf6-40eb-bbce-6251e6ba0300.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32328;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=bvr31726PWD=kfLl5kN6a9PhHdgN;','','')
     
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/signup', methods =['GET', 'POST'])
def signup():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM signup WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            insert_sql = "INSERT INTO signup VALUES(?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully signedup!'
            return render_template('register.html',msg=msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('signup.html', msg=msg)


@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
    if request.method == 'POST' :
        email = request.form['eamil']
        password = request.form['password']
        sql = "SELECT * FROM signup WHERE email =? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        if not(account):
            session['loggedin'] = True
            session['id'] = account['EMAIL']
            userid=  account['EMAIL']
            session['email'] = account['EMAIL']
            msg = 'Logged in successfully !'
            return render_template('home.html', msg = msg)
        else:
               msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

         
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        height = request.form['height']
        weight = request.form['weight']
        age = request.form['age']
        illness = request.form['illness']
        gender = request.form['gender']
        allergies = request.form['allergy']
        sql = "SELECT * FROM profile WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if not(account):
            insert_sql = "INSERT INTO  profile VALUES (?, ?, ?, ?, ?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, height)
            ibm_db.bind_param(prep_stmt, 3, weight)
            ibm_db.bind_param(prep_stmt, 4, age)
            ibm_db.bind_param(prep_stmt, 5, illness)
            ibm_db.bind_param(prep_stmt, 6, gender)
            ibm_db.bind_param(prep_stmt, 7, allergies)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered !'
            return render_template('main.html', msg = msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)


@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/card')
def card():
    sql = "SELECT * FROM ingrediant WHERE almonds =?"
    stmt = ibm_db.exec_immediate(conn, sql)
    tuple = ibm_db.fetch_tuple(stmt)
    while tuple != False:
        print (" Measure: ", tuple[0])
        print (" Grams: ", tuple[1])
        print (" Calories: ", tuple[2])
        print (" Protien: ", tuple[3])
        print (" Fat: ", tuple[4])
        print (" Sat.Fat: ", tuple[5])
        print (" Fiber: ", tuple[6])
        print (" Carbs: ", tuple[7])
        print (" Category: ", tuple[8])
        tuple = ibm_db.fetch_tuple(stmt)
    return render_template('card.html')

if __name__ == '__main__':
   app.run(debug=True)