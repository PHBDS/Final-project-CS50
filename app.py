import secrets
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL



# Configure application
app = Flask(__name__)

# Set a secure secret key
app.secret_key = secrets.token_hex(16)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///shopping.db")



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in, flash invalid login or password"""
    session.clear()
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            message="Incorrect username or password"
            message_type = "warning"

            return redirect(url_for('login', message=message, message_type=message_type))

        # Ensure password was submitted
        elif not request.form.get("password"):
            message="Incorrect username or password"
            message_type = "warning"

            return redirect(url_for('login', message=message,message_type=message_type))

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            message="Incorrect username or password"
            message_type = "warning"

            return redirect(url_for('login', message=message, message_type=message_type))


        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # close any exhisting session
    session.clear()

    # when posting
    if request.method == "POST":

        # check submissions
        for i in ["username", "password", "confirmation"]:
            if not request.form.get(i):
                message="must provide "+i
                message_type = "warning"


                return redirect( url_for('register', message=message,message_type=message_type))


        if request.form.get("password") != request.form.get("confirmation"):
                message= "Confirmation not matching"
                message_type = "warning"

                return redirect(url_for('register', message=message,message_type=message_type))
        
        if len(db.execute("SELECT * FROM users WHERE USERNAME =?", request.form.get("username"))) != 0:
                message = "Username already in use"
                message_type = "warning"

                return redirect( url_for('register', message=message,message_type=message_type))

        # update database

        db.execute("INSERT INTO users (username, hash) VALUES (?,?)", request.form.get(
            "username"), generate_password_hash(request.form.get("password")))

        # start session and go to /
        session["user_id"] = db.execute(
            "SELECT * FROM users WHERE USERNAME =?", request.form.get("username"))[0]["id"]
        
        return redirect("/")

    # when GET
    else:
        return render_template("register.html")







@app.route("/", methods=["GET", "POST"])
@login_required
def index():


    
    if request.method == "POST":
        #if new item form
        if 'new_item' in request.form:
            add_item=request.form.get("product")
            add_category=request.form.get("category")
            if not add_item:
                # If  item is empty, redirect back with an error message
                message = "Must provide item name"
                message_type = "warning"
                return redirect(url_for('index', message=message, message_type=message_type))
            if not add_category:
                # If category is empty, write it as undefined
                add_category="undefined"
 
            add_quantity = request.form.get("quantity") if request.form.get("quantity") else "some"

            #check if category do not exhist, create a new one
            category_count = db.execute("SELECT COUNT(ID) FROM category WHERE UPPER(category) = UPPER(:category) AND user_id = :user_id",
                                        category=add_category, user_id=session["user_id"])[0]['COUNT(ID)']    
            if  category_count == 0 :

                db.execute("INSERT INTO category (user_id, category) VALUES( :user_id, :category  )",
                       user_id= session["user_id"], category= add_category)
            #get category id
            cat_id = db.execute("SELECT id FROM category WHERE  UPPER(category)  =  UPPER(:category) AND user_id = :user_id"
                       ,category=add_category, user_id=session["user_id"] )[0]['id']
            #if product already exist, just change qty
            item_count = db.execute("SELECT COUNT(ID) FROM items WHERE category_id = :cat_id AND user_id = :user_id AND UPPER(item) = UPPER(:item)",
                                    cat_id=cat_id, user_id=session["user_id"], item=add_item)[0]['COUNT(ID)']

            if item_count != 0:
                db.execute("UPDATE items SET qty = :qty WHERE  category_id  =  :category_id AND user_id= :user_id AND  UPPER(item) =  UPPER(:item)",
                    user_id=session["user_id"], 
                    category_id=cat_id, 
                    item=add_item, 
                    qty=add_quantity)
        
            else:  #add new prodcut to database           
                db.execute(
                    "INSERT INTO items (user_id, category_id, item, qty) VALUES (:user_id, :category_id, :item, :qty)",
                    user_id=session["user_id"], 
                    category_id=cat_id, 
                    item=add_item, 
                    qty=add_quantity)
        
        
        
        elif 'mark_as_bought' in request.form:
            item_id = request.form.get("item_id")
            category_id = request.form.get("category_id")
            user_id = session["user_id"]
            item_name = request.form.get("item")

            if item_id and category_id and user_id:
                # Check if the item exists with the given category_id and user_id
                item_exists = db.execute(
                    "SELECT COUNT(*) FROM items WHERE id = :item_id AND category_id = :category_id AND user_id = :user_id",
                    item_id=item_id, category_id=category_id, user_id=user_id
                )[0]['COUNT(*)']

                if item_exists >= 0:
                    # Update the item's quantity to 0
                    db.execute(
                        "UPDATE items SET qty = '0' WHERE id = :item_id AND user_id = :user_id AND category_id = :category_id ",
                        item_id=item_id, user_id=user_id, category_id=category_id
                    )
                    message= item_name + " marked as bought!"
                    message_type = "success"

                    return redirect(url_for('index', message=message,message_type=message_type))
                else:
                    message= item_name + " Something went wrong"
                    message_type = "danger"

                    return redirect(url_for('index', message=message,message_type=message_type))
            else:
                message= "Something went wrong"
                message_type = "danger"
     
                return redirect(url_for('index', message=message,message_type=message_type))

        
        
        elif 'update_quantity' in request.form:
            item_id = request.form.get('item_id')
            category_id = request.form.get('category_id')

            item = request.form.get('item')
            user_id = session["user_id"]
            new_quantity = request.form.get("new_quantity") if request.form.get("new_quantity") else "some"
            
            item_exists = db.execute(
                    "SELECT COUNT(*) FROM items WHERE id = :item_id AND category_id = :category_id AND user_id = :user_id",
                    item_id=item_id, category_id=category_id, user_id=user_id)[0]['COUNT(*)']
            if item_exists >= 0:
                db.execute(
                            "UPDATE items SET qty = :new_quantity WHERE id = :item_id AND user_id = :user_id AND category_id = :category_id ",
                            new_quantity=new_quantity,item_id=item_id, user_id=user_id, category_id=category_id)
                message= item + " placed on the shopping list"
                message_type = "success"

                return redirect(url_for('index', message=message,message_type=message_type))
            else:
                message= item + " not found"
                message_type = "danger"

                return redirect(url_for('index', message=message,message_type=message_type))
        
        elif 'delete_item' in request.form:
            item_id = request.form.get('item_id')
            category_id = request.form.get('category_id')
            user_id = session["user_id"]

            if item_id and category_id:
                # Delete the item
                db.execute("DELETE FROM items WHERE id = :item_id AND user_id = :user_id",
                           item_id=item_id, user_id=user_id)

                # Check if the category is empty
                category_empty = db.execute("SELECT COUNT(*) FROM items WHERE category_id = :category_id",
                                            category_id=category_id)[0]['COUNT(*)']

                if category_empty == 0:
                    # Delete the category if no items are left
                    db.execute("DELETE FROM category WHERE id = :category_id AND user_id = :user_id",
                               category_id=category_id, user_id=user_id)

                message = "Item deleted successfully!"
                message_type = "success"

                return redirect(url_for('index', message=message, message_type=message_type))
                            
       
       
       
       
       # Query the database to get all items for the current user
        products = db.execute("""
            SELECT items.id AS item_id, category_id, category.category, items.item, items.qty
            FROM items
            JOIN category ON items.category_id = category.id
            WHERE items.user_id = :user_id AND items.qty != '0'
            ORDER BY category.category, items.item
        """, user_id=session["user_id"])
        bought_products = db.execute("""
            SELECT items.id AS item_id, category_id, category.category, items.item, items.qty
            FROM items
            JOIN category ON items.category_id = category.id
            WHERE items.user_id = :user_id AND items.qty = '0'
            ORDER BY category.category, items.item
        """, user_id=session["user_id"])
        # Render the template and pass the products to it
        categories=db.execute("SELECT DISTINCT category from category WHERE user_id =:user_id",
                        user_id=session["user_id"])
        categories = [category['category'] for category in categories]
        return render_template("index.html", products=products,bought_products=bought_products,categories=categories)           
        
    else:
        products = db.execute("""
            SELECT items.id AS item_id, category_id, category.category, item, qty
            FROM items
            JOIN category ON items.category_id = category.id
            WHERE items.user_id = :user_id AND items.qty != '0'
            ORDER BY category.category, items.item
        """, user_id=session["user_id"])
        bought_products = db.execute("""
            SELECT items.id AS item_id, category_id, category.category, item, qty
            FROM items
            JOIN category ON items.category_id = category.id
            WHERE items.user_id = :user_id AND items.qty = '0'
            ORDER BY category.category, items.item
        """, user_id=session["user_id"])
        # Render the template and pass the products to it
        categories=db.execute("SELECT DISTINCT category from category WHERE user_id =:user_id",
                        user_id=session["user_id"])
        categories = [category['category'] for category in categories]
        return render_template("index.html", products=products,bought_products=bought_products,categories=categories ) 