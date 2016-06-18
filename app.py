"""
	SIMPLE FLASK BASED APPLICATION
"""



from flask import (Flask, render_template, request, redirect, url_for)
import sqlite3

# app is instance of Flask class
print(__name__) #-->Prints in the terminal 
app = Flask(__name__)

#connecting to db
def get_connection():
	return sqlite3.connect('db.sqlite3')



#initializing db
def init_db():
	db_conn = get_connection()
	cur = db_conn.cursor()
	_sql = '''SELECT name FROM sqlite_master 
	WHERE type ='table' and name='peoples' 
	'''
	cur.execute(_sql)
	if not cur.fetchone():
		_create_sql = '''CREATE TABLE peoples(
			id integer PRIMARY KEY AUTOINCREMENT,
			firstname text NOT NULL,
			lastname text NULL,
			address text NULL,
			country text NULL)
		'''
		cur.execute(_create_sql)
		db_conn.commit()



@app.route('/') #--->Decorator
def index():
	return render_template('home.jinja2') 

@app.route('/hello/<name>')
@app.route('/hello/')
def hello(name=''):
	"""Says hello to users """
	return "Hello {}!".format(name)


@app.route('/add', methods=['GET','POST'])
def add_people():
	"""
	Show add form
	"""
	if request.method == 'POST':
		#save data to database
		db_conn = get_connection()
		cur = db_conn.cursor()
		print ('>'*10, request.form)

		firstname = request.form['first-name']
		lastname = request.form['last-name']
		address = request.form['address']
		country = request.form['country']

		# if firstname is not empty, insert into table:
		if firstname.strip():
			_add_sql = '''
			INSERT INTO peoples(firstname, lastname, address, country)
			 VALUES(?,?,?,?)
			'''
			cur.execute(_add_sql, (firstname.strip(),
				lastname.strip(), address.strip(), country.strip()
			))
			db_conn.commit()
			
			#redirect to list page
			return redirect(url_for('list_people'))
		else:
			#redirect to add page with error
			return redirect(url_for('add_people'))
		
	return render_template('add.jinja2')


@app.route('/list')
def list_people():
	"""
	List all people
	"""
	db_conn = get_connection()
	cur = db_conn.cursor()

	_list_sql = '''
	SELECT id, firstname,lastname,address,country FROM peoples
	'''
	cur.execute(_list_sql)
	values = cur.fetchall()
	print(values)
	return render_template('list.jinja2',data = values)
	
@app.route('/delete/<int:id>')
def delete_people(id):
	db_conn = get_connection()
	cur = db_conn.cursor()
	delete_id = request.form['id']
	print(delete_id)
	_delete_sql = ''' DELETE from peoples where id = delete_id
	'''
	cur.execute(_delete_sql)
	return redirect(url_for('list_people'))




# @app.route('/hello/<name>')
# @app.route('/hello/')
# def hello(name=''):
# 	"""Says hello to users """
# 	return "Hello {}!".format(name)

# @app.route('/details/<int:user_id>')
# def user_details(user_id):
# 	"""
# 		return user detail for the given user
# 	"""
# 	return "{FullName},{Age},{Location}".format(**{
# 		'FullName':'John Doe',
# 		'Age':'23',
# 		'Location':'Ktm'
# 	})

if __name__ =='__main__':
	# only when __name__ is __main__
	init_db()
	app.run(debug = True)

