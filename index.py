from flask import Flask, redirect, url_for, request, render_template, flash, session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'python_etr'

app.secret_key = 'JAUS4LCEDO'

mysql = MySQL(app)

@app.route('/login', methods = ['GET', 'POST'])
def show_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if not email:
            flash('Email is required. Please enter your email.', 'danger')
            return render_template('login.html')
        elif not password:
            flash('Please enter your password.', 'danger')
            return render_template('login.html')
        else:
            try:
                cursor = mysql.connection.cursor()
                cursor.execute('SELECT * FROM USERS WHERE email = %s AND password = %s', (email, password))
                user = cursor.fetchone()
                cursor.close()
                if user:
                    session['user'] = email
                    session['firstName'] = user[1]
                    session['lastName'] = user[2]
                    return redirect('/')
                else:
                    flash('Invalid credentials', 'danger')
                    return render_template('login.html')
            except Exception as e:
                flash(f'Encountered an error: {e}', 'danger')
                return render_template('login.html')
    else:
        if 'user' in session:
            return redirect('/')
        else:
            return render_template('login.html')

@app.route('/')
def home():
    if 'user' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('show_login'))

@app.route('/about')
def about():
    if 'user' in session:
        return render_template('about.html')
    else:
        return redirect(url_for('show_login'))

@app.route('/products')
def show_products():
    if 'user' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()
        cursor.close()
        return render_template('products.html', products = products)
    else:
        return redirect(url_for('show_login'))

@app.route('/add', methods = ['POST'])
def add():
    try:
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        stock = request.form['stock']
        category = request.form['category']
        status = request.form['status']
        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO products (name, description, price, stock, category, status) VALUES (%s, %s, %s, %s, %s, %s)', (name, description, price, stock, category, status))
        mysql.connection.commit()
        cursor.close()
        flash(f'Successfully added {name} to products!', 'success')
        return redirect(url_for('show_products'))
    except Exception as e:
        flash(f'Error adding product: {e}', 'danger')
        return redirect(url_for('show_products'))

@app.route('/save', methods=['POST'])
def save():
    try:
        product_id = request.form['editProductId']
        name = request.form['editName']
        description = request.form['editDescription']
        price = request.form['editPrice']
        stock = request.form['editStock']
        category = request.form['editCategory']
        status = request.form['editStatus']
        
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE products SET name = %s, description = %s, price = %s, stock = %s, category = %s, status = %s WHERE product_id = %s', (name, description, price, stock, category, status, product_id))
        mysql.connection.commit()
        cursor.close()
        flash(f'Successfully edited {name}!', 'success')
        return redirect(url_for('show_products'))
    except Exception as e:
        flash(f'Error editing product: {e}', 'danger')
        return redirect(url_for('show_products'))

@app.route('/delete', methods = ['POST'])
def delete():
    try:
        product_id = request.form['deleteProductId']
        name = request.form['deleteProductName']
        
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM products WHERE product_id = %s', (product_id))
        mysql.connection.commit()
        cursor.close()
        flash(f'Successfully deleted {name}!', 'success')
        return redirect(url_for('show_products'))
    except Exception as e:
        flash(f'Error deleting product: {e}', 'danger')
        return redirect(url_for('show_products'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('show_login'))

if __name__ == '__main__':
    app.run(debug = True)