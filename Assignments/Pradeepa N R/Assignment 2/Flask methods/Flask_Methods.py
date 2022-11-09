from flask import *  
app = Flask(__name__)  
  
  
@app.route('/get',methods = ['GET'])  
def login():  
      uname=request.args.get('uname')  
      passwrd=request.args.get('pass')  
      if uname=="user" and passwrd=="user":  
          return "GET method Working"  

@app.route('/post',methods = ['POST'])  
def login1():  
      uname=request.form['uname']  
      passwrd=request.form['pass']  
      if uname=="user" and passwrd=="user":  
          return "POST method Working"  

@app.route('/put',methods = ['PUT'])  
def login2():  
      uname=request.form['uname']  
      passwrd=request.form['pass']  
      if uname=="user" and passwrd=="user":  
          return "PUT method Working"  

@app.route('/delete',methods = ['DELETE'])  
def login3():  
      uname=request.form['uname']  
      passwrd=request.form['pass']  
      if uname=="user" and passwrd=="user":  
          return "DELETE method Working" 
   
if __name__ == '__main__':  
   app.run(debug = True)  