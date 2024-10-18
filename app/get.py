from datetime import datetime, timedelta
import sqlite3
import calendar



def create_daily_sales():
	today = datetime.now().date()
	conn = sqlite3.connect('products.db')
	cursor = conn.cursor()
	quantity = 0
	total_price = 0

	purchase_time = datetime.now().time()
	purchase_datetime = datetime.combine(today, purchase_time)
	ref_id = f"sl-{purchase_datetime.strftime('%Y%m%d-%H%M%S')}"


	cursor.execute('SELECT * FROM sales WHERE date = ?', (today,))
	if cursor.fetchone() is None:
		cursor.execute('''
		INSERT INTO sales (date, quantity, total_price, reference) 
		VALUES (?, ?, ?, ?) ''', 
		(today, quantity, total_price, ref_id)) 

	conn.commit()
	conn.close()

create_daily_sales()

def get_dashboard_values():

	conn = sqlite3.connect('products.db')
	cursor = conn.cursor()

	today = datetime.now().date()

	dashboard_values = []
	cursor.execute("""
		SELECT total_price
		FROM sales
		WHERE date = ?
		""", (today,))
	dashboard_values.append(cursor.fetchone()[0])

	cursor.execute("""
		SELECT quantity
		FROM sales
		WHERE date = ?
		""", (today,))
	dashboard_values.append(cursor.fetchone()[0])

	cursor.execute("""
		SELECT SUM(quantity)
		FROM products
		""" )
	dashboard_values.append(cursor.fetchone()[0])

	cursor.execute("SELECT MAX(id) FROM purchase")
	last_purchase_id = cursor.fetchone()[0]
	cursor.execute('SELECT quantity FROM purchase WHERE id = ?', (last_purchase_id,))
	dashboard_values.append(cursor.fetchone()[0])

	cursor.execute('SELECT total_price FROM purchase WHERE id = ?', (last_purchase_id,))
	dashboard_values.append(cursor.fetchone()[0])

	cursor.execute("""SELECT COUNT(*) 
		FROM products 
		WHERE quantity < 10;
		""")
	dashboard_values.append(cursor.fetchone()[0])

	# Retrieve the saved date from the database
	cursor.execute("SELECT date FROM sales")  
	saved_date = cursor.fetchone()[0]
	# Convert the saved date to a datetime object
	saved_date = datetime.strptime(saved_date, '%Y-%m-%d').date()

	# Calculate the previous month
	if saved_date.month == 1:
		prev_month = 12
		prev_year = saved_date.year - 1
	else:
		prev_month = saved_date.month - 1
		prev_year = saved_date.year

	# Get the first and last days of the previous month
	first_day_prev_month = datetime(prev_year, prev_month, 1).date()
	last_day_prev_month = datetime(prev_year, prev_month, calendar.monthrange(prev_year, prev_month)[1]).date()

	# Filter records from the previous month
	cursor.execute("SELECT SUM(quantity) FROM sales WHERE date >= ? AND date <= ?", 
               (first_day_prev_month.strftime('%Y-%m-%d'), last_day_prev_month.strftime('%Y-%m-%d')))
	dashboard_values.append(cursor.fetchone()[0])

	# Filter records from the previous month
	cursor.execute("SELECT SUM(total_price) FROM sales WHERE date >= ? AND date <= ?", 
               (first_day_prev_month.strftime('%Y-%m-%d'), last_day_prev_month.strftime('%Y-%m-%d')))
	dashboard_values.append(cursor.fetchone()[0])

	# Retrieve the last 5 inserted names
	cursor.execute("SELECT products FROM sales_items ORDER BY rowid DESC LIMIT 1")
	dashboard_values.append(cursor.fetchall())

	conn.close()
	return dashboard_values

def fillChart():
	# Connect to the database
	conn = sqlite3.connect('products.db')
	cursor = conn.cursor()

	# Retrieve the sales data from the last 10 days
	cursor.execute("SELECT date, quantity FROM sales WHERE date >= ?", ((datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),))
	sales_data = cursor.fetchall()

	# Close the connection
	conn.close()

	data = {
	    'labels': [],
	    'datasets': [{
	        'label': 'Sales',
	        'data': [],
	        'borderColor': 'rgba(255, 99, 132, 1)',
	        'fill': False
	    }]
	}

	for row in sales_data:
		data['labels'].append(row[0])
		data['datasets'][0]['data'].append(row[1])

	return data
