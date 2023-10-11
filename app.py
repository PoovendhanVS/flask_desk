import mysql.connector
from flask import Flask, redirect, render_template, request, url_for
from flask import session
from fileinput import filename
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

# Debug code : 291-145-463
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

def capitalize_first(value):
    return value.capitalize()

app.jinja_env.filters['capitalize_first'] = capitalize_first

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'flask_db',
}
def get_db_connection():
    return mysql.connector.connect(**db_config)


@app.route('/')
def login():
    return render_template('index.html')

@app.route('/get_login', methods = ['POST'])
def get_login():
    if request.method == "POST":
        name = request.form['name']
        pwd = request.form['pwd']
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "SELECT * FROM user_creation WHERE user_name = %s AND password = %s"
        cursor.execute(sql,(name, pwd))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result:
            session['user_id'] = result[0]
            session['user_type_id'] = result[1]
            session['user_name'] = result[2]
            session['email_id'] = result[3]
        return 'Success'
    else:
        return 'Error'

@app.route('/dashboard')
def index():
    if 'user_name' in session:
        session_name = session['user_name']
        return render_template('index1.html', session_name = session_name)
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    if 'user_name' in session:
        session.clear()
        return redirect('/')
    else:
        return redirect('/logout')

#  User Creation
#  Start
@app.route('/signup')
def signup():
    if 'user_name' in session:
        session_name = session['user_name']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT user_type_id, user_type_name FROM user_type_creation')
        user_type_names = cursor.fetchall()
        return render_template('user/create.html', session_name = session_name, user_type_names = user_type_names)
    else:
        return redirect('/logout')

@app.route('/user_creation')
def user_list():
    if 'user_name' in session:
        session_name = session['user_name']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
                SELECT  user.user_id, user.user_name, user_type.user_type_name, user.email_id
                FROM user_creation AS user
                LEFT JOIN user_type_creation AS user_type
                ON user.user_type_id = user_type.user_type_id
                WHERE user.delete_status != 1
         """)
        result = cursor.fetchall()
        
        return render_template('user/admin.html',session_name = session_name, result = result)
    else:
        return redirect('/logout')

@app.route('/user_create',methods = ['POST'])
def user_create():
    if 'user_name' in session:
        if request.method == 'POST':
            user_type = request.form['usertype']
            user_name = request.form['name']
            email = request.form['email']
            pwd = request.form['pwd']
            
            if (user_name  != '') & (email != '') & (pwd != ''):
                connection = get_db_connection()
                cursor = connection.cursor()
                sql = "INSERT INTO user_creation (user_type_id, user_name, email_id, password) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (user_type, user_name, email, pwd))
                connection.commit()
                cursor.close()
                connection.close()
                return 'Success'
                
            else:
                return "Empty Field"
    else:
        return redirect('/logout')
    
@app.route('/update_user/<id>')
def update_user(id):
    if 'user_name' in session:
        session_name = session['user_name']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT user_type_id, user_type_name FROM user_type_creation')
        user_type_names = cursor.fetchall()
        if id != '':
            connection = get_db_connection()
            cursor = connection.cursor()
            sql = "SELECT * FROM user_creation WHERE user_id = %s"
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            cursor.close()
            connection.close()
            return render_template('user/update.html',row = row, session_name = session_name, user_type_names = user_type_names)
    else:
        return redirect('/logout')
            
@app.route('/edit_user', methods=['POST'])
def edit_user():
    if 'user_name' in session:
        if request.method == 'POST':
            usertype = request.form['usertype']
            id = request.form['user_id']
            name = request.form['name']
            email = request.form['email']
            pwd = request.form['pwd']
            if name != '' and email != '' and pwd != '':
                connection = get_db_connection()
                cursor = connection.cursor()
                sql = "UPDATE user_creation SET user_type_id = %s, user_name = %s, email_id = %s, password = %s WHERE user_id = %s"
                cursor.execute(sql, (usertype, name, email, pwd, id))
                connection.commit()
                cursor.close()
                connection.close()
                return 'Success'
        else:
            return 'Invalid data'
    else:
        return redirect('/logout')
            
@app.route('/delete_user/<id>')
def delete_user(id):
    if 'user_name' in session:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "UPDATE user_creation SET delete_status = %s WHERE user_id= %s"
        cursor.execute(sql, (1, id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect('/user_creation')
    else:
        return redirect('/logout')

# End

# User Type Creation
# Start

@app.route('/user_type_creation')
def user_type_creation():
    if 'user_name' in session:
        session_name = session['user_name']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_type_creation WHERE delete_status != 1")
        result = cursor.fetchall()
        return render_template('user_type_creation/admin.html', session_name=session_name, result= result)
    else:
        return redirect('/logout')
    
@app.route('/create_user_type')
def create_user_type():
    session_name = session['user_name']
    allstatus = ['Active', 'Inactive']
    return render_template('user_type_creation/create.html',  session_name=session_name, allstatus=allstatus)

@app.route('/insert_user_type', methods = ['POST'])
def insert_user_type():
    if 'user_name' in session:
        if request.method == 'POST':
            user_type = request.form['usertype']
            status = request.form['status']
            if (user_type  != '') & (status != ''):
                connection = get_db_connection()
                cursor = connection.cursor()
                sql = "INSERT INTO user_type_creation (user_type_name, status) VALUES (%s,%s)"
                cursor.execute(sql, (user_type, status))
                connection.commit()
                cursor.close()
                connection.close()
                return 'Success'
            else:
                return 'User Type is required'
    else:
        return redirect('/logout')

@app.route('/update_user_type/<user_type_id>')
def update_user_type(user_type_id):
    if 'user_name' in session:
        session_name = session['user_name']
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "SELECT * FROM user_type_creation WHERE user_type_id = %s"
        cursor.execute(sql,(user_type_id,))
        row = cursor.fetchone()
        return render_template('user_type_creation/update.html',user_type_id=user_type_id,session_name=session_name, row= row)

@app.route('/edit_user_type', methods = ['POST'])
def edit_user_type():
    if 'user_name' in session:
        if request.method == 'POST':
            user_type_id = request.form['id']
            user_type = request.form['name']
            status = request.form['status']
            if (user_type  != '') & (status != ''):
                connection = get_db_connection()
                cursor = connection.cursor()
                sql = "UPDATE user_type_creation SET user_type_name = %s, status= %s WHERE user_type_id = %s"
                cursor.execute(sql, (user_type, status, user_type_id))
                connection.commit()
                cursor.close()
                connection.close()
                return 'Success'
            else:
                return 'User Type is required'
    else:
        return redirect('/logout')

@app.route('/delete_user_type/<id>')
def delete_user_type(id):
    if 'user_name' in session:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "UPDATE user_type_creation SET delete_status = %s WHERE user_type_id= %s"
        cursor.execute(sql, (1, id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect('/user_type_creation')
    else:
        return redirect('/logout')

# End
# Company Creation
# Start
@app.route('/company_creation')
def company_creation():
    if 'user_name' in session:
        session_name = session['user_name']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id,company_name,address,bill_name,bill_address,mobile_no FROM company_details WHERE delete_status != 1")
        result = cursor.fetchall()
        
        return render_template('company_creation/admin.html',session_name=session_name, result = result)
    return redirect(url_for('/logout'))

@app.route('/create_company')
def create_comapny():
    if 'user_name' in session:
        session_name = session['user_name']
        return render_template('company_creation/create.html', session_name=session_name)
    return redirect(url_for('/logout'))

@app.route('/insert_company', methods = ['POST'])
def insert_company():
    if 'user_name' in session:
        if request.method == 'POST':
            com_name = request.form['com_name']
            com_address = request.form['com_address']
            bill_name = request.form['bill_name']
            bill_address = request.form['bill_address']
            mobile = request.form['mobile']
            phone = request.form['phone']
            gst = request.form['gst']
            if(com_name != '') & (com_address != '')&(mobile != '')&(gst != ''):
                connection = get_db_connection()
                cursor = connection.cursor()
                sql = "INSERT INTO company_details (company_name,address,bill_name,bill_address,mobile_no,phone_no,gst_no) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql,(com_name,com_address,bill_name,bill_address,mobile,phone,gst))
                connection.commit()
                cursor.close()
                connection.close()
                return 'Success'
            else:
                return 'All field is requried'
            
@app.route('/update_company/<com_id>')
def update_company(com_id):
    if 'user_name' in session:
        session_name = session['user_name']
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = 'SELECT id,company_name,address,bill_name,bill_address,mobile_no,phone_no,gst_no FROM company_details WHERE id=%s'
        cursor.execute(sql, (com_id,))
        row = cursor.fetchone()
        return render_template('company_creation/update.html',row = row, session_name = session_name)
    else:
        return redirect(url_for('/logout'))

@app.route('/edit_company_details', methods = ['POST'])
def edit_company_details():
    if 'user_name' in session:
        if request.method == 'POST':
            com_id = request.form['com_id']
            com_name = request.form['com_name']
            com_address = request.form['com_address']
            bill_name = request.form['bill_name']
            bill_address = request.form['bill_address']
            mobile = request.form['mobile']
            phone = request.form['phone']
            gst = request.form['gst']
            if com_id != '':
                connection = get_db_connection()
                cursor = connection.cursor()
                sql = "UPDATE company_details SET company_name = %s,address = %s,bill_name = %s,bill_address = %s,mobile_no = %s,phone_no = %s,gst_no = %s  WHERE id=%s"
                cursor.execute(sql, (com_name,com_address,bill_name,bill_address,mobile,phone,gst,com_id))
                connection.commit()
                cursor.close()
                connection.close()
                return 'Success'
            else:
                return 'Feild is empty'
        else:
            pass
@app.route('/delete_company/<com_id>')
def delete_company_details(com_id):
    if 'user_name' in session:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "UPDATE company_details SET delete_status = 1 WHERE id = %s"
        cursor.execute(sql, (com_id,))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect('/company_creation')
    else:
        return redirect('/logout')
        
@app.route('/staff_creation')
def staff_creation():
    if 'user_name' in session:
        session_name = session['user_name']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""SELECT staff.staff_id,staff.staff_no,user_type.user_type_name,staff.staff_name,staff.contact_no,city.city_name 
                    FROM staff_creation as staff
                    LEFT JOIN user_type_creation as user_type ON staff.user_type_id = user_type.user_type_id
                    LEFT JOIN city_name as city ON staff.city_id = city.city_id
                     WHERE staff.delete_status != 1 """)
        result = cursor.fetchall()
        return render_template('staff_creation/admin.html',session_name=session_name, result=result)
    return redirect(url_for('/logout'))

@app.route('/delete_staff/<staff_id>')
def delete_staff(staff_id):
    if 'user_name' in session:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = 'UPDATE staff_creation SET delete_status = 1 WHERE staff_id = %s'
        cursor.execute(sql, (staff_id,))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect('/staff_creation')    

# End
if __name__ == ('__main__'):
    app.run(debug=True)

# # 
# def name():
#     if 'user_name' in session:
#         session_name = session['user_name']
#         return render_template('address', session_name=session_name)
#     return redirect(url_for('/'))