#flask app
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL 


app = Flask(__name__)
app.secret_key='123456789'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB']='SMS'

mysql = MySQL(app)



@app.route('/index')
def index():
    cur= mysql.connection.cursor()
    result_val=cur.execute("SELECT * FROM users")
    if result_val>0:
        userDetails=cur.fetchall()
        print(userDetails)
        return render_template('index.html',userDetails=userDetails)
    


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if len(email)<4:
            flash('email must be greater than 4 characters',category='error')
        elif len(password)<4:
            flash('password must be greater than 4 characters',category='error')
        else:
      
            cur= mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE email=%s",(email,))
            user_exists=cur.fetchone()
            if user_exists:
                flash('email already exists',category='error')
            else:    
                cur.execute("INSERT INTO users (email,password) VALUES (%s, %s)", (email, password))
                mysql.connection.commit()
                cur.close() 
                flash('student added',category='success')
                return redirect(url_for('add'))

        
    return render_template('add.html')

@app.route('/')
def update():
    return 'UPDATE'


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        id = request.form.get('id')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE id=%s",(id,))
        user_exists=cur.fetchone()
        if not user_exists:
            flash('student does not exist',category='error')
        else:    
            cur.execute("DELETE FROM users WHERE id=%s",(id,))
            mysql.connection.commit()
            cur.close()
            flash('student deleted',category='success')
            return redirect(url_for('delete'))


    return render_template('delete.html')




if __name__ == '__main__':
    app.run(debug=True)
