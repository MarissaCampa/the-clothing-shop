<<<<<<< HEAD
import sqlite3
import datetime
import os
from flask import Flask, flash, redirect, render_template, request, session, g, current_app, url_for
from flask_session import Session
from flask_uploads import UploadSet, configure_uploads, IMAGES
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from helpers import apology, login_required, db_query, add_order_to_db, show_category
from forms import RegistrationForm, LoginForm, OrderForm, AddProduct

# Configure application
app = Flask(__name__)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/image/product'
app.config['UPLOADED_PHOTOS_ALLOW'] = set(['.png','.jpg','.jpeg'])
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    form = OrderForm(request.form)    
    query = 'SELECT * FROM products WHERE category = ? ORDER BY RANDOM() LIMIT 4'

    tops = db_query(query=query, args=['tops'])
    dress = db_query(query=query, args=['dress'])
    handbags = db_query(query=query, args=['handbags'])
    shoes = db_query(query=query, args=['shoes'])
    sweaters = db_query(query=query, args=['sweaters'])

    return render_template("home.html", tops=tops, dress=dress, handbags=handbags, shoes=shoes, sweaters=sweaters, form=form)

    # query = 'SELECT * FROM products ORDER BY RANDOM() LIMIT 4'
    # products = db_query(query=query)

    # return render_template("home.html", products=products, form=form)


@app.route("/login", methods = ["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()
    # Get object of the class LoginForm from the "login" route form
    form = LoginForm(request.form)

    # User reached route via POST (as by submitting a form via POST)
    if request.method == 'POST' and form.validate():

        # Get username from login form
        username = form.username.data
        
        # Query SQL users table with entered username
        query = 'SELECT * FROM users WHERE username = ?'
        user = db_query(query=query, args=[username], one=True)

        if user is None:
            flash('User not found', 'danger')
            return render_template("login.html", form=form)     
        
        if not check_password_hash(user['hash'], form.password.data):
            session['logged_in'] = False
            flash('Incorrect password', 'danger')
            return render_template("login.html", form=form)     

        else:
            # Remember which user has logged in
            session['uid'] = user['uid']
            session['username'] = username
            session['logged_in'] = True
            next_url = request.form.get("next")

            if next_url:    
                # Return to previous url (passed to "login.html")
                return redirect(next_url)

            # Redirect user to home page
            return redirect("/")

    else:
        return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    """ Log user out """

    # Forget any user session
    session.clear()

    # Redirect user to main page
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    """ User Registration"""

    session.clear()

    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = generate_password_hash(form.password.data)

        query = "INSERT INTO users (username, hash) VALUES (?, ?)"
        args = (username, password)
        _ = db_query(query=query, args=args)

        flash('Thanks for registering', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)


@app.route('/dress', methods=['GET', 'POST'])
def dress():
    category = 'dress'
    header = 'Dresses'

    form = OrderForm(request.form)
    query = 'SELECT * FROM products WHERE category=? ORDER BY pid ASC'
    products = db_query(query, args=[category])
    
    if request.method == 'POST' and form.validate():
        add_order_to_db(request=request, form=form)
        flash('Order successful', 'success')
        return render_template('category.html', products=products, form=form, header='Dresses', category=category)

    if 'view' in request.args:
        product_id = request.args['view']
        query = 'SELECT * FROM products WHERE pid = ?'
        product_view = db_query(query, args=[product_id])
        return render_template('view_product.html', x='', product_view=product_view)

    elif 'order' in request.args:
        product_id = request.args['order']
        if not 'logged_in' in session:
            session['next'] = url_for(category, order=product_id)
            return redirect(url_for('login', next=request.url))

        query = 'SELECT * FROM products WHERE pid = ?'
        product_order = db_query(query, args=[product_id])
        return render_template('order_product.html', x='', product_order=product_order, form=form)

    return render_template('category.html', products=products, form=form, header=header, category=category)

@app.route('/handbags', methods=['GET', 'POST'])
def handbags():
    category = 'handbags'
    header = 'Handbags'

    form = OrderForm(request.form)
    query = 'SELECT * FROM products WHERE category=? ORDER BY pid ASC'
    products = db_query(query, args=[category])
    
    if request.method == 'POST' and form.validate():
        add_order_to_db(request=request, form=form)
        flash('Order successful', 'success')
        return render_template('category.html', products=products, form=form, header='Dresses', category=category)

    if 'view' in request.args:
        product_id = request.args['view']
        query = 'SELECT * FROM products WHERE pid = ?'
        product_view = db_query(query, args=[product_id])
        return render_template('view_product.html', x='', product_view=product_view)

    elif 'order' in request.args:
        product_id = request.args['order']
        if not 'logged_in' in session:
            session['next'] = url_for(category, order=product_id)
            return redirect(url_for('login', next=request.url))

        query = 'SELECT * FROM products WHERE pid = ?'
        product_order = db_query(query, args=[product_id])
        return render_template('order_product.html', x='', product_order=product_order, form=form)

    return render_template('category.html', products=products, form=form, header=header, category=category)


@app.route('/shoes', methods=['GET', 'POST'])
def shoes():
    category = 'shoes'
    header = 'Shoes'

    form = OrderForm(request.form)
    query = 'SELECT * FROM products WHERE category=? ORDER BY pid ASC'
    products = db_query(query, args=[category])
    
    if request.method == 'POST' and form.validate():
        add_order_to_db(request=request, form=form)
        flash('Order successful', 'success')
        return render_template('category.html', products=products, form=form, header='Dresses', category=category)

    if 'view' in request.args:
        product_id = request.args['view']
        query = 'SELECT * FROM products WHERE pid = ?'
        product_view = db_query(query, args=[product_id])
        return render_template('view_product.html', x='', product_view=product_view)

    elif 'order' in request.args:
        product_id = request.args['order']
        if not 'logged_in' in session:
            session['next'] = url_for(category, order=product_id)
            return redirect(url_for('login', next=request.url))

        query = 'SELECT * FROM products WHERE pid = ?'
        product_order = db_query(query, args=[product_id])
        return render_template('order_product.html', x='', product_order=product_order, form=form)

    return render_template('category.html', products=products, form=form, header='Shoes', category=category)


@app.route('/sweaters', methods=['GET', 'POST'])
def sweaters():
    category = 'sweaters'
    header = 'Sweaters'

    form = OrderForm(request.form)
    query = 'SELECT * FROM products WHERE category=? ORDER BY pid ASC'
    products = db_query(query, args=[category])
    
    if request.method == 'POST' and form.validate():
        add_order_to_db(request=request, form=form)
        flash('Order successful', 'success')
        return render_template('category.html', products=products, form=form, header='Dresses', category=category)

    if 'view' in request.args:
        product_id = request.args['view']
        query = 'SELECT * FROM products WHERE pid = ?'
        product_view = db_query(query, args=[product_id])
        return render_template('view_product.html', x='', product_view=product_view)

    elif 'order' in request.args:
        product_id = request.args['order']
        if not 'logged_in' in session:
            session['next'] = url_for(category, order=product_id)
            return redirect(url_for('login', next=request.url))

        query = 'SELECT * FROM products WHERE pid = ?'
        product_order = db_query(query, args=[product_id])
        return render_template('order_product.html', x='', product_order=product_order, form=form)

    return render_template('category.html', products=products, form=form, header=header, category=category)


@app.route('/tops', methods=['GET', 'POST'])
def tops():
    category = 'tops'
    header = 'Tops'

    form = OrderForm(request.form)
    query = 'SELECT * FROM products WHERE category=? ORDER BY pid ASC'
    products = db_query(query, args=[category])
    
    if request.method == 'POST' and form.validate():
        add_order_to_db(request=request, form=form)
        flash('Order successful', 'success')
        return render_template('category.html', products=products, form=form, header='Dresses', category=category)

    if 'view' in request.args:
        product_id = request.args['view']
        query = 'SELECT * FROM products WHERE pid = ?'
        product_view = db_query(query, args=[product_id])
        return render_template('view_product.html', x='', product_view=product_view)

    elif 'order' in request.args:
        product_id = request.args['order']
        if not 'logged_in' in session:
            session['next'] = url_for(category, order=product_id)
            return redirect(url_for('login', next=request.url))

        query = 'SELECT * FROM products WHERE pid = ?'
        product_order = db_query(query, args=[product_id])
        return render_template('order_product.html', x='', product_order=product_order, form=form)

    return render_template('category.html', products=products, form=form, header=header, category=category)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'uid' in request.args and not 'orders' in request.args:
        uid = request.args['uid']
        query = 'SELECT * FROM users WHERE uid = ?'
        user = db_query(query=query, args=[uid], one=True)
        return render_template('profile.html', user=user)

    elif 'uid' in request.args and 'orders' in request.args:
        uid = request.args['uid']
        query = """SELECT p1.uid, p1.pid, p1.quantity, p1.oname, p1.mobile, p1.address, strftime('%d/%m/%Y', p1.ddate) as ddate, 
                          p2.pname, p2.price, p2.category, p2.picture, p2.price * p1.quantity as totalprice
                    FROM orders p1 INNER JOIN products p2
                    ON (p1.pid = p2.pid AND p1.uid = ?)"""
        orders = db_query(query=query, args=[uid])
        return render_template('orders.html', orders=orders)

    return redirect('/')


@app.route('/search', methods=['POST', 'GET'])
def search():
    if 'q' in request.args:
        q = request.args['q']

        query = """SELECT * FROM products WHERE pname LIKE ? ORDER BY pid ASC"""
        products = db_query(query=query, args=['%' + q + '%'])

        if products is None:
            flash('Search again', 'danger')
            return render_template('search.html')
        else:
            flash('Showing results for: ' + q, 'success')
            return render_template('search.html', products=products)

    return redirect('/')



@app.route('/admin_add_product', methods=['POST', 'GET'])
# @is_admin_logged_in
def admin_add_product():
    form = AddProduct(request.form)

    if request.method == 'POST':
        if form.validate():
            file = request.files['picture']
            if file:
                pic = file.filename
                photo = pic.replace("'","")
                picture = photo.replace(" ", "_")
                if picture.lower().endswith(('.png','.jpg','.jpeg')):
                    (_, ext) = os.path.splitext(picture)
                    file.filename = str(form.pcode.data) + ext
                    picture = file.filename
                    category = form.category.data
                    save_photo = photos.save(file, folder=category, name=picture)
                    if save_photo:
                        query = """INSERT INTO products(pid,pname,price,description,available,category,picture)
                                    VALUES(?,?,?,?,?,?,?)"""
                        args = (form.pcode.data,
                                form.pname.data, 
                                str(form.price.data),
                                form.description.data, 
                                form.available.data, 
                                form.category.data, 
                                picture)
                        _ = db_query(query=query, args=args)

                        query = 'INSERT INTO product_level (pid) VALUES(?)'
                        _ = db_query(query=query, args=[form.pcode.data])

                        levels = request.form.getlist(category)
                        for lev in levels:
                            yes = 'yes'
                            query = 'UPDATE product_level SET {field} = ? WHERE pid = ?'.format(field=lev)
                            args = (yes, form.pcode.data)
                            _ = db_query(query=query, args=args)
                        flash('Product added successful', 'success')

                    else:
                        flash('Could not save picture. Try again', 'danger')
                else:
                    flash('Picture format must be png or jpg', 'danger')
            else:
                flash('No file found', 'danger')
        else:
            flash('Form not validated', 'danger')        

    return render_template('admin/add_product.html', form=form)


@app.route('/edit_product', methods=['POST', 'GET'])
# @is_admin_logged_in
def edit_product():
    if 'id' in request.args:
        product_id = request.args['id']
        curso = mysql.connection.cursor()
        res = curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        curso.execute("SELECT * FROM product_level WHERE product_id=%s", (product_id,))
        product_level = curso.fetchall()
        if res:
            if request.method == 'POST':
                name = request.form.get('name')
                price = request.form['price']
                description = request.form['description']
                available = request.form['available']
                category = request.form['category']
                item = request.form['item']
                code = request.form['code']
                file = request.files['picture']
                # Create Cursor
                if name and price and description and available and category and item and code and file:
                    pic = file.filename
                    photo = pic.replace("'", "")
                    picture = photo.replace(" ", "")
                    if picture.lower().endswith(('.png', '.jpg', '.jpeg')):
                        file.filename = picture
                        save_photo = photos.save(file, folder=category)
                        if save_photo:
                            # Create Cursor
                            cur = mysql.connection.cursor()
                            exe = curso.execute(
                                "UPDATE products SET pName=%s, price=%s, description=%s, available=%s, category=%s, item=%s, pCode=%s, picture=%s WHERE id=%s",
                                (name, price, description, available, category, item, code, picture, product_id))
                            if exe:
                                if category == 'tshirt':
                                    level = request.form.getlist('tshirt')
                                    for lev in level:
                                        yes = 'yes'
                                        query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                                            field=lev)
                                        cur.execute(query, (yes, product_id))
                                        # Commit cursor
                                        mysql.connection.commit()
                                elif category == 'wallet':
                                    level = request.form.getlist('wallet')
                                    for lev in level:
                                        yes = 'yes'
                                        query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                                            field=lev)
                                        cur.execute(query, (yes, product_id))
                                        # Commit cursor
                                        mysql.connection.commit()
                                elif category == 'belt':
                                    level = request.form.getlist('belt')
                                    for lev in level:
                                        yes = 'yes'
                                        query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                                            field=lev)
                                        cur.execute(query, (yes, product_id))
                                        # Commit cursor
                                        mysql.connection.commit()
                                elif category == 'shoes':
                                    level = request.form.getlist('shoes')
                                    for lev in level:
                                        yes = 'yes'
                                        query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                                            field=lev)
                                        cur.execute(query, (yes, product_id))
                                        # Commit cursor
                                        mysql.connection.commit()
                                else:
                                    flash('Product level not fund', 'danger')
                                    return redirect(url_for('admin_add_product'))
                                flash('Product updated', 'success')
                                return redirect(url_for('edit_product'))
                            else:
                                flash('Data updated', 'success')
                                return redirect(url_for('edit_product'))
                        else:
                            flash('Pic not upload', 'danger')
                            return render_template('pages/edit_product.html', product=product,
                                                   product_level=product_level)
                    else:
                        flash('File not support', 'danger')
                        return render_template('pages/edit_product.html', product=product,
                                               product_level=product_level)
                else:
                    flash('Fill all field', 'danger')
                    return render_template('pages/edit_product.html', product=product,
                                           product_level=product_level)
            else:
                return render_template('pages/edit_product.html', product=product, product_level=product_level)
        else:
            return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_login'))

=======
import sqlite3
import datetime
import os
from flask import Flask, flash, redirect, render_template, request, session, g, current_app, url_for
from flask_session import Session
from flask_uploads import UploadSet, configure_uploads, IMAGES
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from helpers import apology, login_required, db_query, add_order_to_db, show_category
from forms import RegistrationForm, LoginForm, OrderForm, AddProduct

# Configure application
app = Flask(__name__)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/image/product'
app.config['UPLOADED_PHOTOS_ALLOW'] = set(['.png','.jpg','.jpeg'])
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    form = OrderForm(request.form)    
    query = 'SELECT * FROM products WHERE category = ? ORDER BY RANDOM() LIMIT 4'

    tops = db_query(query=query, args=['tops'])
    dress = db_query(query=query, args=['dress'])
    handbags = db_query(query=query, args=['handbags'])
    shoes = db_query(query=query, args=['shoes'])
    sweaters = db_query(query=query, args=['sweaters'])

    return render_template("home.html", tops=tops, dress=dress, handbags=handbags, shoes=shoes, sweaters=sweaters, form=form)

    # query = 'SELECT * FROM products ORDER BY RANDOM() LIMIT 4'
    # products = db_query(query=query)

    # return render_template("home.html", products=products, form=form)


@app.route("/login", methods = ["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()
    # Get object of the class LoginForm from the "login" route form
    form = LoginForm(request.form)

    # User reached route via POST (as by submitting a form via POST)
    if request.method == 'POST' and form.validate():

        # Get username from login form
        username = form.username.data
        
        # Query SQL users table with entered username
        query = 'SELECT * FROM users WHERE username = ?'
        user = db_query(query=query, args=[username], one=True)

        if user is None:
            flash('User not found', 'danger')
            return render_template("login.html", form=form)     
        
        if not check_password_hash(user['hash'], form.password.data):
            session['logged_in'] = False
            flash('Incorrect password', 'danger')
            return render_template("login.html", form=form)     

        else:
            # Remember which user has logged in
            session['uid'] = user['uid']
            session['username'] = username
            session['logged_in'] = True
            next_url = request.form.get("next")

            if next_url:    
                # Return to previous url (passed to "login.html")
                return redirect(next_url)

            # Redirect user to home page
            return redirect("/")

    else:
        return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    """ Log user out """

    # Forget any user session
    session.clear()

    # Redirect user to main page
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    """ User Registration"""

    session.clear()

    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = generate_password_hash(form.password.data)

        query = "INSERT INTO users (username, hash) VALUES (?, ?)"
        args = (username, password)
        _ = db_query(query=query, args=args)

        flash('Thanks for registering', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)


@app.route('/dress', methods=['GET', 'POST'])
def dress():
    category = 'dress'
    header = 'Dresses'

    form = OrderForm(request.form)
    query = 'SELECT * FROM products WHERE category=? ORDER BY pid ASC'
    products = db_query(query, args=[category])
    
    if request.method == 'POST' and form.validate():
        add_order_to_db(request=request, form=form)
        flash('Order successful', 'success')
        return render_template('category.html', products=products, form=form, header='Dresses', category=category)

    if 'view' in request.args:
        product_id = request.args['view']
        query = 'SELECT * FROM products WHERE pid = ?'
        product_view = db_query(query, args=[product_id])
        return render_template('view_product.html', x='', product_view=product_view)

    elif 'order' in request.args:
        product_id = request.args['order']
        if not 'logged_in' in session:
            session['next'] = url_for(category, order=product_id)
            return redirect(url_for('login', next=request.url))

        query = 'SELECT * FROM products WHERE pid = ?'
        product_order = db_query(query, args=[product_id])
        return render_template('order_product.html', x='', product_order=product_order, form=form)

    return render_template('category.html', products=products, form=form, header=header, category=category)

@app.route('/handbags', methods=['GET', 'POST'])
def handbags():
    category = 'handbags'
    header = 'Handbags'

    form = OrderForm(request.form)
    query = 'SELECT * FROM products WHERE category=? ORDER BY pid ASC'
    products = db_query(query, args=[category])
    
    if request.method == 'POST' and form.validate():
        add_order_to_db(request=request, form=form)
        flash('Order successful', 'success')
        return render_template('category.html', products=products, form=form, header='Dresses', category=category)

    if 'view' in request.args:
        product_id = request.args['view']
        query = 'SELECT * FROM products WHERE pid = ?'
        product_view = db_query(query, args=[product_id])
        return render_template('view_product.html', x='', product_view=product_view)

    elif 'order' in request.args:
        product_id = request.args['order']
        if not 'logged_in' in session:
            session['next'] = url_for(category, order=product_id)
            return redirect(url_for('login', next=request.url))

        query = 'SELECT * FROM products WHERE pid = ?'
        product_order = db_query(query, args=[product_id])
        return render_template('order_product.html', x='', product_order=product_order, form=form)

    return render_template('category.html', products=products, form=form, header=header, category=category)


@app.route('/shoes', methods=['GET', 'POST'])
def shoes():
    category = 'shoes'
    header = 'Shoes'

    form = OrderForm(request.form)
    query = 'SELECT * FROM products WHERE category=? ORDER BY pid ASC'
    products = db_query(query, args=[category])
    
    if request.method == 'POST' and form.validate():
        add_order_to_db(request=request, form=form)
        flash('Order successful', 'success')
        return render_template('category.html', products=products, form=form, header='Dresses', category=category)

    if 'view' in request.args:
        product_id = request.args['view']
        query = 'SELECT * FROM products WHERE pid = ?'
        product_view = db_query(query, args=[product_id])
        return render_template('view_product.html', x='', product_view=product_view)

    elif 'order' in request.args:
        product_id = request.args['order']
        if not 'logged_in' in session:
            session['next'] = url_for(category, order=product_id)
            return redirect(url_for('login', next=request.url))

        query = 'SELECT * FROM products WHERE pid = ?'
        product_order = db_query(query, args=[product_id])
        return render_template('order_product.html', x='', product_order=product_order, form=form)

    return render_template('category.html', products=products, form=form, header='Shoes', category=category)


@app.route('/sweaters', methods=['GET', 'POST'])
def sweaters():
    category = 'sweaters'
    header = 'Sweaters'

    form = OrderForm(request.form)
    query = 'SELECT * FROM products WHERE category=? ORDER BY pid ASC'
    products = db_query(query, args=[category])
    
    if request.method == 'POST' and form.validate():
        add_order_to_db(request=request, form=form)
        flash('Order successful', 'success')
        return render_template('category.html', products=products, form=form, header='Dresses', category=category)

    if 'view' in request.args:
        product_id = request.args['view']
        query = 'SELECT * FROM products WHERE pid = ?'
        product_view = db_query(query, args=[product_id])
        return render_template('view_product.html', x='', product_view=product_view)

    elif 'order' in request.args:
        product_id = request.args['order']
        if not 'logged_in' in session:
            session['next'] = url_for(category, order=product_id)
            return redirect(url_for('login', next=request.url))

        query = 'SELECT * FROM products WHERE pid = ?'
        product_order = db_query(query, args=[product_id])
        return render_template('order_product.html', x='', product_order=product_order, form=form)

    return render_template('category.html', products=products, form=form, header=header, category=category)


@app.route('/tops', methods=['GET', 'POST'])
def tops():
    category = 'tops'
    header = 'Tops'

    form = OrderForm(request.form)
    query = 'SELECT * FROM products WHERE category=? ORDER BY pid ASC'
    products = db_query(query, args=[category])
    
    if request.method == 'POST' and form.validate():
        add_order_to_db(request=request, form=form)
        flash('Order successful', 'success')
        return render_template('category.html', products=products, form=form, header='Dresses', category=category)

    if 'view' in request.args:
        product_id = request.args['view']
        query = 'SELECT * FROM products WHERE pid = ?'
        product_view = db_query(query, args=[product_id])
        return render_template('view_product.html', x='', product_view=product_view)

    elif 'order' in request.args:
        product_id = request.args['order']
        if not 'logged_in' in session:
            session['next'] = url_for(category, order=product_id)
            return redirect(url_for('login', next=request.url))

        query = 'SELECT * FROM products WHERE pid = ?'
        product_order = db_query(query, args=[product_id])
        return render_template('order_product.html', x='', product_order=product_order, form=form)

    return render_template('category.html', products=products, form=form, header=header, category=category)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'uid' in request.args and not 'orders' in request.args:
        uid = request.args['uid']
        query = 'SELECT * FROM users WHERE uid = ?'
        user = db_query(query=query, args=[uid], one=True)
        return render_template('profile.html', user=user)

    elif 'uid' in request.args and 'orders' in request.args:
        uid = request.args['uid']
        query = """SELECT p1.uid, p1.pid, p1.quantity, p1.oname, p1.mobile, p1.address, strftime('%d/%m/%Y', p1.ddate) as ddate, 
                          p2.pname, p2.price, p2.category, p2.picture, p2.price * p1.quantity as totalprice
                    FROM orders p1 INNER JOIN products p2
                    ON (p1.pid = p2.pid AND p1.uid = ?)"""
        orders = db_query(query=query, args=[uid])
        return render_template('orders.html', orders=orders)

    return redirect('/')


@app.route('/search', methods=['POST', 'GET'])
def search():
    if 'q' in request.args:
        q = request.args['q']

        query = """SELECT * FROM products WHERE pname LIKE ? ORDER BY pid ASC"""
        products = db_query(query=query, args=['%' + q + '%'])

        if products is None:
            flash('Search again', 'danger')
            return render_template('search.html')
        else:
            flash('Showing results for: ' + q, 'success')
            return render_template('search.html', products=products)

    return redirect('/')



@app.route('/admin_add_product', methods=['POST', 'GET'])
# @is_admin_logged_in
def admin_add_product():
    form = AddProduct(request.form)

    if request.method == 'POST':
        if form.validate():
            file = request.files['picture']
            if file:
                pic = file.filename
                photo = pic.replace("'","")
                picture = photo.replace(" ", "_")
                if picture.lower().endswith(('.png','.jpg','.jpeg')):
                    (_, ext) = os.path.splitext(picture)
                    file.filename = str(form.pcode.data) + ext
                    picture = file.filename
                    category = form.category.data
                    save_photo = photos.save(file, folder=category, name=picture)
                    if save_photo:
                        query = """INSERT INTO products(pid,pname,price,description,available,category,picture)
                                    VALUES(?,?,?,?,?,?,?)"""
                        args = (form.pcode.data,
                                form.pname.data, 
                                str(form.price.data),
                                form.description.data, 
                                form.available.data, 
                                form.category.data, 
                                picture)
                        _ = db_query(query=query, args=args)

                        query = 'INSERT INTO product_level (pid) VALUES(?)'
                        _ = db_query(query=query, args=[form.pcode.data])

                        levels = request.form.getlist(category)
                        for lev in levels:
                            yes = 'yes'
                            query = 'UPDATE product_level SET {field} = ? WHERE pid = ?'.format(field=lev)
                            args = (yes, form.pcode.data)
                            _ = db_query(query=query, args=args)
                        flash('Product added successful', 'success')

                    else:
                        flash('Could not save picture. Try again', 'danger')
                else:
                    flash('Picture format must be png or jpg', 'danger')
            else:
                flash('No file found', 'danger')
        else:
            flash('Form not validated', 'danger')        

    return render_template('admin/add_product.html', form=form)


@app.route('/edit_product', methods=['POST', 'GET'])
# @is_admin_logged_in
def edit_product():
    if 'id' in request.args:
        product_id = request.args['id']
        curso = mysql.connection.cursor()
        res = curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        curso.execute("SELECT * FROM product_level WHERE product_id=%s", (product_id,))
        product_level = curso.fetchall()
        if res:
            if request.method == 'POST':
                name = request.form.get('name')
                price = request.form['price']
                description = request.form['description']
                available = request.form['available']
                category = request.form['category']
                item = request.form['item']
                code = request.form['code']
                file = request.files['picture']
                # Create Cursor
                if name and price and description and available and category and item and code and file:
                    pic = file.filename
                    photo = pic.replace("'", "")
                    picture = photo.replace(" ", "")
                    if picture.lower().endswith(('.png', '.jpg', '.jpeg')):
                        file.filename = picture
                        save_photo = photos.save(file, folder=category)
                        if save_photo:
                            # Create Cursor
                            cur = mysql.connection.cursor()
                            exe = curso.execute(
                                "UPDATE products SET pName=%s, price=%s, description=%s, available=%s, category=%s, item=%s, pCode=%s, picture=%s WHERE id=%s",
                                (name, price, description, available, category, item, code, picture, product_id))
                            if exe:
                                if category == 'tshirt':
                                    level = request.form.getlist('tshirt')
                                    for lev in level:
                                        yes = 'yes'
                                        query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                                            field=lev)
                                        cur.execute(query, (yes, product_id))
                                        # Commit cursor
                                        mysql.connection.commit()
                                elif category == 'wallet':
                                    level = request.form.getlist('wallet')
                                    for lev in level:
                                        yes = 'yes'
                                        query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                                            field=lev)
                                        cur.execute(query, (yes, product_id))
                                        # Commit cursor
                                        mysql.connection.commit()
                                elif category == 'belt':
                                    level = request.form.getlist('belt')
                                    for lev in level:
                                        yes = 'yes'
                                        query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                                            field=lev)
                                        cur.execute(query, (yes, product_id))
                                        # Commit cursor
                                        mysql.connection.commit()
                                elif category == 'shoes':
                                    level = request.form.getlist('shoes')
                                    for lev in level:
                                        yes = 'yes'
                                        query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                                            field=lev)
                                        cur.execute(query, (yes, product_id))
                                        # Commit cursor
                                        mysql.connection.commit()
                                else:
                                    flash('Product level not fund', 'danger')
                                    return redirect(url_for('admin_add_product'))
                                flash('Product updated', 'success')
                                return redirect(url_for('edit_product'))
                            else:
                                flash('Data updated', 'success')
                                return redirect(url_for('edit_product'))
                        else:
                            flash('Pic not upload', 'danger')
                            return render_template('pages/edit_product.html', product=product,
                                                   product_level=product_level)
                    else:
                        flash('File not support', 'danger')
                        return render_template('pages/edit_product.html', product=product,
                                               product_level=product_level)
                else:
                    flash('Fill all field', 'danger')
                    return render_template('pages/edit_product.html', product=product,
                                           product_level=product_level)
            else:
                return render_template('pages/edit_product.html', product=product, product_level=product_level)
        else:
            return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_login'))

>>>>>>> main
