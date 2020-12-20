import mariadb
from flask import Flask, request, Response
import json
import dbcreds
from flask_cors import CORS
import random
import string

app = Flask(__name__)
CORS(app)
def generateToken():
  letters = string.ascii_letters
  result_str = ''.join(random.choice(letters)for i in range (40))
  return result_str


#Login Endpoint, visitors should be able to login or create an account. 
@app.route("/api/login", methods =["POST", "DELETE"])   
def loginendpoint():
    if request.method == "POST":
      conn = None
      cursor = None 
      user_password = request.json.get("password")
      user_email = request.json.get("email")
      rows = None
      user = None
      try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database,)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE password=? AND email=?", [user_password, user_email,])
        user = cursor.fetchall()
        print(user)
        rows = cursor.rowcount
        if (rows == 1):
          cursor.execute("INSERT INTO session(user_id, login_token) VALUES (?,?)", [user[0], generateToken(),])
          conn.commit()
          rows = cursor.rowcount
      except Exception as error:
        print("Something went wrong: ")
        print(error)   
      finally:
        if(cursor != None):
         cursor.close()
        if(conn != None):
         conn.rollback()
         conn.close()
        if(rows == 1):
          return Response("User login successfull!", mimetype="text/html", status=201)
        else:
          return Response("Information entered is not valid!", mimetype="text/html", status=500)
    elif request.method == "DELETE":
      conn = None
      cursor = None 
      user = None
      user_loginToken = request.json.get("loginToken")
      rows = None
      try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database,)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM session WHERE login_token=?", [user_loginToken,])
        conn.commit()
        rows = cursor.rowcount
      except Exception as error:
        print("Something went wrong: ")
        print(error)     
      finally:
        if(cursor != None):
         cursor.close()
        if(conn != None):
         conn.rollback()
         conn.close()
        if(rows == 1):
          return Response("Delete Success!", mimetype="text/html", status=204)
        else:
          return Response("Login token invalid!", mimetype="text/html", status=500) 
# User Endpoint          
@app.route("/api/user", methods =["GET", "POST","DELETE"])
def userendpoint():
    if request.method == "GET":
      conn = None
      cursor = None
      user = None
      user = request.json.get("user")
      rows = None
      try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database,)
        cursor = conn.cursor()
        if user != "" and user != None:
          cursor.execute("SELECT * FROM user WHERE id = ?", [id,])
        else:
          cursor.execute("SELECT * FROM user")
        user = cursor.fetchall()
      except Exception as error:
        print("Something went wrong(: ")
        print(error)   
      finally:
        if(cursor != None):
         cursor.close()
        if(conn != None):
         conn.rollback()
         conn.close()
        if(user != None):
            return Response(json.dumps(user, default=str), mimetype="application/json", status=200)
        else:
            return Response("User does not exist.", mimetype="text/html", status=500) 
    elif request.method == "POST": 
      conn = None
      cursor = None 
      user_username = request.json.get("username")
      user_password = request.json.get("password")
      user_email = request.json.get("email")
      loginToken = generateToken()
      rows = None
      try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database,)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user(username, password, email) VALUES (?, ?, ?)", [user_username, user_password, user_email,])
        conn.commit()
        rows = cursor.rowcount
        if(rows == 1):
          user = cursor.lastrowid
          cursor.execute("INSERT INTO session(user_id, login_token) VALUES (?,?)", [user, loginToken])
          conn.commit()
          rows = cursor.rowcount      
      except Exception as error:
        print("Something went wrong: ")
        print(error)   
      finally:
        if(cursor != None):
         cursor.close()
        if(conn != None):
         conn.rollback()
         conn.close()
        if(rows == 1):
          user = {
             "loginToken": loginToken,
             "userId": user
          }
          return Response(json.dumps(user, default=str), mimetype="text/html", status=201)
        else:
          return Response("Username or email already exists!", mimetype="text/html", status=500)
    elif request.method == "DELETE":
      conn = None
      cursor = None 
      user_password = request.json.get("password")
      user_loginToken = request.json.get("loginToken")
      rows = None
      try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database,)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM session WHERE login_token=?", [user_loginToken,])
        user = cursor.fetchone()
        print(user)
        cursor.execute("DELETE FROM user WHERE id=? AND password=?", [user[0], user_password,])
        conn.commit()
        rows = cursor.rowcount
      except Exception as error:
        print("Something went wrong: ")
        print(error)     
      finally:
        if(cursor != None):
         cursor.close()
        if(conn != None):
         conn.rollback()
         conn.close()
        if(rows == 1):
          return Response("Delete Success!", mimetype="text/html", status=204)
        else:
          return Response("Login token or password not valid!", mimetype="text/html", status=500)
#Recipe Post endpoint
@app.route("/api/recipe_post", methods =["GET", "POST","DELETE"])
def recipepostendpoint():        
    if request.method == "GET":
      conn = None
      cursor = None
      user = None
      user_id = request.args.get("user_id")
      rows = None
      try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database,)
        cursor = conn.cursor()
        if user != "" and user != None:
          cursor.execute("SELECT content FROM recipe_post WHERE id = ?", [user_id,])
        else:
          cursor.execute("SELECT * FROM recipe_post")
          user = cursor.fetchall()
      except Exception as error:
        print("Something went wrong: ")
        print(error)   
      finally:
        if(cursor != None):
         cursor.close()
        if(conn != None):
         conn.rollback()
         conn.close()
        if(user != None):
            return Response(json.dumps(user, default=str), mimetype="application/json", status=200)
        else:
            return Response("Post does not exist.", mimetype="text/html", status=500)
    elif request.method == "POST": 
      conn = None
      cursor = None 
      user_loginToken = request.json.get("loginToken")
      recipe_post_content = request.json.get("content")
      rows = None
      try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database,)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM session WHERE login_token=?", [user_loginToken,])
        user = cursor.fetchone()
        rows = cursor.rowcount 
        cursor.execute("INSERT INTO recipe_post(content, user_id) VALUES (?,?)", [recipe_post_content, user[0],])
        conn.commit()
        rows = cursor.rowcount
      except Exception as error:
        print("Something went wrong: ")
        print(error)   
      finally:
        if(cursor != None):
         cursor.close()
        if(conn != None):
         conn.rollback()
         conn.close()
        if(rows == 1):
          return Response("Recipe posted successfully!", mimetype="text/html", status=201)
        else:
          return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "DELETE":
      conn = None
      cursor = None 
      user_loginToken = request.json.get("loginToken")
      rows = None
      try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database,)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM session WHERE login_token=?", [user_loginToken,])
        user = cursor.fetchone()
        print(user)
        cursor.execute("DELETE FROM recipe_post WHERE id=?", [user[0],])
        conn.commit()
        rows = cursor.rowcount
      except Exception as error:
        print("Something went wrong: ")
        print(error)     
      finally:
        if(cursor != None):
         cursor.close()
        if(conn != None):
         conn.rollback()
         conn.close()
        if(rows == 1):
          return Response("Delete Success!", mimetype="text/html", status=204)
        else:
          return Response("Login token or password not valid!", mimetype="text/html", status=500)        




