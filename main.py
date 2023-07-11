import pymysql
from app import app
from config import mysql
from flask import request, json, jsonify, flash

#get data member
@app.route('/member')
def member():
    try:
        conn      = mysql.connect()
        cursor    = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery  = "SELECT * FROM an_member WHERE 1=1"
        cursor.execute(sqlQuery)
        empRows   = cursor.fetchall()
        respone   = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

#get data member detail
@app.route('/member/<int:id>')
def memberDetails(id):
    try:
        conn    = mysql.connect()
        cursor  = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT id, name, email, type, type_status, package FROM an_member WHERE id =%s"
        cursor.execute(sqlQuery, id)
        empRow  = cursor.fetchone()
        respone = jsonify(empRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 
        
#created data member
@app.route('/member/create', methods=['POST'])
def create_emp():
    try:        
        _json   = request.json
        _name   = _json['name']
        _email  = _json['email']
        if _name and _email and request.method == 'POST':
            conn      = mysql.connect()
            cursor    = conn.cursor(pymysql.cursors.DictCursor)		
            sqlQuery  = "INSERT INTO emp(name, email, phone, address) VALUES(%s, %s, %s, %s)"
            bindData  = (_name, _email)            
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Member added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 

#update data member
@app.route('/member/update', methods=['PUT'])
def memberUpdate():
    try:
        _json = request.json
        _id       = _json['id']
        _name     = _json['name']
        _email    = _json['email']
        if _name and _email and _id and request.method == 'PUT':			
            sqlQuery  = "UPDATE an_member SET name=%s, email=%s, phone=%s, address=%s WHERE id=%s"
            bindData  = (_name, _email, _id)
            conn      = mysql.connect()
            cursor    = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone   = jsonify('Member updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/member/delete/<int:id>', methods=['DELETE'])
def deleteMember(id):
	try:
		conn      = mysql.connect()
		cursor    = conn.cursor()
		cursor.execute("DELETE FROM an_member WHERE id =%s", (id,))
		conn.commit()
		respone   = jsonify('Member deleted successfully!')
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
       
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
        
if __name__ == "__main__":
    app.run()