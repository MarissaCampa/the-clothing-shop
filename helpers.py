import sqlite3
import datetime
from sqlite3 import Error
from flask import Flask, flash, jsonify, redirect, render_template, request, session, g, current_app
from flask.cli import with_appcontext
from functools import wraps

from forms import RegistrationForm, LoginForm, OrderForm, AddProduct


# SQLite3 Helper Functions
DATABASE = 'database.db'

def get_db():
        db = getattr(g, '_database', None)
        if db is None:
                db = g._database = sqlite3.connect(DATABASE)
        return db

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def db_query(query, args=(), one=False):
    rv = []
    try:
        with sqlite3.connect(DATABASE) as con:
            con.row_factory = make_dicts
            cur = con.cursor()
            cur.execute(query, args)
            con.commit()
            rv = cur.fetchall()
    except Error as e:
        print(e)

    return (rv[0] if rv else None) if one else (rv if rv else None)


def apology(message, code=400):
        """Render message as an apology to user."""
        def escape(s):
                """
                Escape special characters.

                https://github.com/jacebrowning/memegen#special-characters
                """
                for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                                                 ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
                        s = s.replace(old, new)
                return s
        return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
        """
        Decorate routes to require login.

        http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
                if session.get("user_id") is None:
                        return redirect("/login")
                return f(*args, **kwargs)
        return decorated_function


def add_order_to_db(request, form):
    try:
        oname = form.name.data
        mobile = form.mobile_num.data
        address = form.order_place.data
        pid = request.args['order']
        quantity = form.quantity.data
        now = datetime.datetime.now()
        week = datetime.timedelta(days=7)
        delivery_date = now + week
        ddate = delivery_date
        # ddate = delivery_date.strftime('%y-%m-%d %H:%M:%S')

        if 'uid' in session:
            uid = session['uid']
            query = 'INSERT INTO orders (uid, oname, mobile, address, pid, quantity, ddate)' \
                    'VALUES (?,?,?,?,?,?,?)'
            args = (uid, oname, mobile, address, pid, quantity, ddate) 
            _ = db_query(query=query, args=args)
        else:
            return redirect('/login')

    except Error as e:
        print(e)


def show_category(category, request):

    form = OrderForm(request.form)
    query = 'SELECT * FROM products WHERE category=? ORDER BY pid ASC'
    products = db_query(query, args=[category])
    
    if request.method == 'POST' and form.validate():
        add_order_to_db(request=request, form=form)
        flash('Order successful', 'success')
        return render_template(category + '.html', products=products, form=form)

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

    return render_template(category + '.html', products=products, form=form)
