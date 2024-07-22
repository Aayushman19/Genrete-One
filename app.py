from flask import Flask
from flask import render_template
from flask import request
import psycopg2
import requests

app = Flask(__name__)
def get_connection():
	try:
		return psycopg2.connect(
			database="users",
			user="postgres",
			password="",
			host="localhost",
			port=5432,
		)
	except:
		return False
	
url = "https://pizza-and-desserts.p.rapidapi.com/pizzas/"

headers = {
	"x-rapidapi-key": "70eb31faa0msh7d050807db2aaa4p1212bejsnbc5a59d3a4c6",
	"x-rapidapi-host": "pizza-and-desserts.p.rapidapi.com"
}
	
@app.route('/homepage')
def home():
	pizza = request.form['dish']
	url = url+str(pizza)
	response = requests.get(url, headers=headers)
	return render_template('home.html', response = response)

@app.route('/bill')
def index():
	conn = get_connection()
	if not conn:
		return f"db not connected"
	curr = conn.cursor()
	curr.execute('select * from restaurant_billing')
	orders = curr.fetchall()
	curr.close()
	conn.close()
	return render_template('food.html', orders = orders)

if __name__ == '__main__':
	app.run()