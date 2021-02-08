import pyodbc
import os
from flask import Flask,redirect,render_template,request
import pypyodbc
import time
import random
import urllib
import datetime
import json
import redis
import pickle
import hashlib

app = Flask(__name__)

img_folder = os.path.join('static','images')
app.config['UPLOAD_FOLDER'] = img_folder
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

server = 'shivam-db0.database.windows.net'
database = 'app1-db'
username = 'shivam'
password = 'qwerty@1'
driver = '{ODBC Driver 17 for SQL Server}'
myHostname = "manifin.redis.cache.windows.net"
myPassword = "aGqEGVxHVMtweNAOOvacdDuyTQcMpgu90vQSA8u3N8g="

r = redis.Redis(host='manifin.redis.cache.windows.net',
        port=6380, db=0, password='aGqEGVxHVMtweNAOOvacdDuyTQcMpgu90vQSA8u3N8g=', ssl=True)

def print_hi2():
    with pyodbc.connect(
            'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT TOP 3 name, collation_name FROM sys.databases")
            row = cursor.fetchone()
            while row:
                print(str(row[0]) + " " + str(row[1]))
                row = cursor.fetchone()


# Retrieving a user's Img from the DB
@app.route('/getUserImg', methods=['GET'])
def getUserImg():
    uname = request.args.get('userName', '')
    print(uname)
    imagelist = ['images/' + uname + '.jpg']
    return render_template ("getUserImg.html", imagelist=imagelist)

#  Adding picture for a user
@app.route('/addPicforUser', methods=['POST'])
def addPicture():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('removedUserConfirmationPg.html')



# Removing a user from the DB
@app.route('/removeUser', methods=['GET'])
def removeUser():
    uname = request.args.get('user_to_remove', '')
    con = pypyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = con.cursor()
    query = "delete from dbo.people2 where name='" + uname +"'"
    print(query)
    cursor.execute(query)
    con.commit()
    print('Removed')
    return render_template('removedUserConfirmationPg.html')



# Updating the keyword for user
@app.route('/updateKeyword', methods=['GET'])
def updateKeyword():
    uname = request.args.get('userName', '')
    newKeyword = request.args.get('keyword_to_change','')
    con = pypyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = con.cursor()
    query = "update dbo.people2 set Keywords='"+ newKeyword +"' where name='" + uname +"'"
    print(query)
    cursor.execute(query)
    con.commit()
    print('updated Keyword')
    return render_template('keywordUpdatedConfirmationPg.html')


# Updating the salary for user
@app.route('/updateSalary', methods=['GET'])
def updateSalary():
    uname = request.args.get('userName', '')
    newSal = request.args.get('new_sal','')
    con = pypyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = con.cursor()
    query = "update dbo.people2 set Salary='"+ newSal +"' where name='" + uname +"'"
    print(query)
    cursor.execute(query)
    con.commit()
    print('Updated Salary')
    return render_template('SalaryUpdatedConfirmationPg.html')

@app.route('/')
def index():
    # Use a breakpoint in the code line below to debug your script.
    print('Hi')  # Press Ctrl+F8 to toggle the breakpoint.
    return render_template('index.html')





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run()

