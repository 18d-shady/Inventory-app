from flask import render_template, request, jsonify, url_for, redirect
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequestKeyError
import requests
import sqlite3
from datetime import datetime
import os
from app import app
from app import get
import json



# Create a directory to store the uploaded images
uploadFolder = 'images'
UPLOAD_FOLDER = os.path.join(app.static_folder, uploadFolder)
#print(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/')
def index():
	return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
	dashboard_values = []
	dashboard_values = get.get_dashboard_values()
	return render_template("dashboard.html", dashboard_values=dashboard_values)

@app.route('/fill_chart')
def fillChart():
	data = {}
	data = get.fillChart()
	return jsonify(data)

@app.route('/get_low_stock')
def lowStock():
	conn = sqlite3.connect('products.db')
	cursor = conn.cursor()
	cursor.execute("""SELECT id, name, quantity 
		FROM products 
		WHERE quantity < 10;
		""")
	rows = cursor.fetchall()
	conn.close()
	return jsonify([{'product_id': item[0], 'name': item[1], 'quantity': item[2]} for item in rows])


@app.route('/products')
def products():
	conn = sqlite3.connect('products.db')
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM products')
	rows = cursor.fetchall()
	"""
	for row in rows:
		print(row)
	"""
	conn.close() 
    
	return render_template("products.html", rows=rows)

@app.route("/add-product", methods=["POST"])
def add_product():

    # Get the image file from the request
	image_file = request.files['product_image']

	# Save the image file to the upload folder
	filename = secure_filename(image_file.filename)
	image_path = filename
	image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


	# Get the other form data from the request
	product_name = request.form['product_name']
	product_code = request.form['product_code']
	product_brand = request.form['product_brand']
	product_quantity = request.form['product_quantity']
	product_price = request.form['product_price']

	conn = sqlite3.connect('products.db')
	cursor = conn.cursor()
	cursor.execute('''
		INSERT INTO products (name, image, code, brand, quantity, price) 
		VALUES (?, ?, ?, ?, ?, ?) ''', 
		(product_name, image_path, product_code, product_brand, product_quantity, product_price)) 
	conn.commit() 
	conn.close() 
	return jsonify({"message": "Product added successfully"})


@app.route("/update-product", methods=["POST"])
def update_product():
	row_id = request.form['row_id']
	# Get the image file from the request
	conn = sqlite3.connect('products.db')
	cursor = conn.cursor()
	# Retrieve the image field value
	try:
		image_file = request.files['product_image']
		# Save the image file to the upload folder
		filename = secure_filename(image_file.filename)
		image_path = filename
		image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		cursor.execute("SELECT image FROM products WHERE id = ?", (row_id,))
		former_image = cursor.fetchone()[0]
		try:
			os.remove(os.path.join(app.config['UPLOAD_FOLDER'], former_image))
		except FileNotFoundError:
			pass
	except BadRequestKeyError:
		cursor.execute("SELECT image FROM products WHERE id = ?", (row_id,))
		image_path = cursor.fetchone()[0]


	# Get the other form data from the request
	product_name = request.form['product_name']
	product_code = request.form['product_code']
	product_brand = request.form['product_brand']
	product_quantity = request.form['product_quantity']
	product_price = request.form['product_price']

	cursor.execute('UPDATE products SET name = ?, image = ?, code = ?, brand = ?, quantity = ?, price = ? WHERE id = ?', (product_name, image_path, product_code, product_brand, product_quantity, product_price, row_id))
	conn.commit() 
	conn.close() 
	return jsonify({"message": "Product updated successfully"})


@app.route("/delete-product", methods=["POST"])
def delete_product():

	# Get the other form data from the request
	row_id = request.form['row_id']
	

	conn = sqlite3.connect('products.db')
	cursor = conn.cursor()
	# Retrieve the image field value
	cursor.execute("SELECT image FROM products WHERE id = ?", (row_id,))
	filename = cursor.fetchone()[0]
	os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	cursor.execute("DELETE FROM products WHERE id = ?", (row_id,))
	cursor.execute("UPDATE products SET id = id - 1 WHERE id > ?", (row_id,))
	conn.commit() 
	conn.close() 
	return jsonify({"message": "Product deleted successfully"})
	


@app.route('/sales')
def sales():
	conn = sqlite3.connect('products.db')
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM sales')
	rows = cursor.fetchall()
	conn.close() 
	return render_template("sales.html", rows=rows)

@app.route('/purchases')
def purchase():
	conn = sqlite3.connect('products.db')
	cursor = conn.cursor()
	cursor.execute('SELECT id, name FROM products')
	productss = cursor.fetchall()

	cursor.execute('SELECT * FROM purchase')
	rows = cursor.fetchall()
	#productss = [row[0] for row in cursor.fetchall()]
	"""
	for row in rows:
		print(row)
	"""
	conn.close() 
    
	return render_template("purchase.html", productss=productss, rows=rows)

@app.route("/add-purchase", methods=["POST"])
def add_purchase():
	values_array = request.get_json()
	if values_array == []:
		return jsonify({"message": "Purchase not added successfully"})
	print(values_array)
	today = datetime.now().date()
	supplier = "Lamed Pharmacy"
	p_status = "Paid"

	purchase_time = datetime.now().time()
	# combine the date and time to create a datetime object
	purchase_datetime = datetime.combine(today, purchase_time)
	ref_id = f"pr-{purchase_datetime.strftime('%Y%m%d-%H%M%S')}"

	conn = sqlite3.connect('products.db')
	cursor = conn.cursor()
	cursor.execute('''
		INSERT INTO purchase (date, supplier, reference, payment_status) 
		VALUES (?, ?, ?, ?) ''', 
		(today, supplier, ref_id, p_status)) 

	conn.commit()
	new_purchase_id = cursor.lastrowid

	for items in values_array:
		product_id = items['selectValue']
		quantity = items['numberValue']
		cursor.execute('''
			INSERT INTO purchase_items (purchase_id, product_id, quantity) 
			VALUES (?, ?, ?) ''', 
			(new_purchase_id, product_id, quantity))

		cursor.execute("""
			UPDATE products
			SET quantity = quantity + ?
			WHERE id = ?
			""", (quantity, product_id))

	conn.commit()

	cursor.execute("""
		SELECT SUM(quantity)
		FROM purchase_items
		WHERE purchase_id = ?
		""", (new_purchase_id,))
	total_quantity = cursor.fetchone()[0]

	cursor.execute("""
		SELECT SUM(pi.quantity * p.price)
		FROM purchase_items pi
		JOIN products p ON pi.product_id = p.id
		WHERE pi.purchase_id = ?
		""", (new_purchase_id,))

	grand_total = cursor.fetchone()[0]

	cursor.execute("""
		UPDATE purchase
		SET quantity = ?, total_price = ?
		WHERE id = ?
		""", (total_quantity, grand_total, new_purchase_id))


	conn.commit() 
	conn.close() 


	return jsonify({"message": "Purchase added successfully"})

@app.route('/get_purchase_items/<int:purchase_id>')
def get_purchase_items(purchase_id):
	conn = sqlite3.connect('products.db')
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM purchase_items WHERE purchase_id = ?', (purchase_id,))
	rows = cursor.fetchall()
	# Prepare a list to hold the results
	results = []
	for item in rows:
		# Fetch the product name for each item
		cursor.execute('SELECT name FROM products WHERE id = ?', (item[2],))
		pName = cursor.fetchone()  # Use fetchone() since we expect a single result

		# Check if pName is not None and extract the name
		product_name = pName[0] if pName else "Unknown Product"

		# Append the result with the product name
		results.append({
			'name': product_name,  # Use the fetched product name
			'quantity': item[3]
			})

	print(rows)
	conn.close()
	return jsonify(results)


@app.route("/delete-purchase", methods=["POST"])
def delete_purchase():

	# Get the other form data from the request
	row_id = request.form['row_id']
	

	conn = sqlite3.connect('products.db')
	cursor = conn.cursor()
	
	cursor.execute("DELETE FROM purchase WHERE id = ?", (row_id,))
	cursor.execute("UPDATE purchase SET id = id - 1 WHERE id > ?", (row_id,))
	cursor.execute("DELETE FROM purchase_items WHERE purchase_id = ?", (row_id,))
	cursor.execute("UPDATE purchase_items SET purchase_id = purchase_id - 1 WHERE purchase_id > ?", (row_id,))
	conn.commit() 
	conn.close() 
	return jsonify({"message": "Purchase deleted successfully"})

@app.route('/pos')
def pos():
	conn = sqlite3.connect('products.db')
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM products')
	rows = cursor.fetchall()
	conn.close() 

	return render_template("pos.html", rows=rows)

@app.route('/new-sales', methods=["POST"])
def new_sales():
	data = request.json
	quantity = ''.join(filter(str.isdigit, data['quantity']))
	quantity = int(quantity)
	total_price = ''.join(filter(str.isdigit, data['total_price']))
	total_price = int(total_price)
	today = datetime.now().date()
	sale_time = datetime.now().time().strftime("%H:%M:%S")
	
	values_array = data['displayedTextData']
	if values_array == []:
		return jsonify({"message": "Purchase not added successfully"})

	conn = sqlite3.connect('products.db')
	cursor = conn.cursor()
	first_list = []
	
	for items in values_array:
		product_id = items['childText']
		single_quantity = items['inputValue']
		cursor.execute("""
			SELECT name
			FROM products
			WHERE id = ?
			""", (product_id,))
		product_name = cursor.fetchone()[0]
		first_list.append(f"{product_name}: {single_quantity}")

		cursor.execute("""
			UPDATE products
			SET quantity = quantity - ?
			WHERE id = ?
			""", (single_quantity, product_id))

	conn.commit()
	product_list = ", ".join(first_list)

	print(product_list)

	cursor.execute("""
		SELECT id
		FROM sales
		WHERE date = ?
		""", (today,))
	sale_id = cursor.fetchone()[0]

	
	cursor.execute('''
		INSERT INTO sales_items (sale_id, total_price, quantity, products, time_bought) 
		VALUES (?, ?, ?, ?, ?) ''', 
		(sale_id, total_price, quantity, product_list, sale_time)) 

	conn.commit()

	cursor.execute("""
		SELECT SUM(quantity)
		FROM sales_items
		WHERE sale_id = ?
		""", (sale_id,))
	total_quantity = cursor.fetchone()[0]
	

	cursor.execute("""
		SELECT SUM(total_price)
		FROM sales_items
		WHERE sale_id = ?
		""", (sale_id,))
	grand_total = cursor.fetchone()[0]
	

	cursor.execute("""
		UPDATE sales
		SET quantity = ?, total_price = ?
		WHERE id = ?
		""", (total_quantity, grand_total, sale_id))

	conn.commit() 

	conn.close()
	#print(values_array)
	return jsonify({"message": "Sales added successfully"})

@app.route('/get_sales_items/<int:sales_id>')
def get_sales_items(sales_id):
	conn = sqlite3.connect('products.db')
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM sales_items WHERE sale_id = ?', (sales_id,))
	rows = cursor.fetchall()
	# Prepare a list to hold the results
	conn.close()
	return jsonify([{'time_bought': item[5], 'description': item[4], 'quantity': item[3], 'total_price': item[2]} for item in rows])


@app.route('/about')
def about():
	return render_template("about.html")



@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

"""
# Get the new maximum ID
cursor.execute("SELECT MAX(id) FROM your_table")
new_max_id = cursor.fetchone()[0]

# Use the new maximum ID + 1 as the ID for the next row
next_row_id = new_max_id + 1
"""