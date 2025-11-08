"""app.py: render and route to webpages"""

import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from db.query import get_all, get_one, insert
from db.server import init_database
from db.schema import Users
import bcrypt
import logging

logging.basicConfig(
    filename="logs/log.txt", level=logging.INFO, filemode="a", format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# load environment variables from .env
load_dotenv()

# database connection - values set in .env
db_name = os.getenv('db_name')
db_owner = os.getenv('db_owner')
db_pass = os.getenv('db_pass')
db_url = f"postgresql://{db_owner}:{db_pass}@localhost/{db_name}"

def create_app():
    """Create Flask application and connect to your DB"""
    # create flask app
    app = Flask(__name__, 
                template_folder=os.path.join(os.getcwd(), 'templates'), 
                static_folder=os.path.join(os.getcwd(), 'static'))
    
    # connect to db
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    
    # Initialize database
    with app.app_context():
        if not init_database():
            print("Failed to initialize database. Exiting.")
            exit(1)

    # ===============================================================
    # routes
    # ===============================================================

    # create a webpage based off of the html in templates/index.html
    @app.route('/')
    def index():
        """Home page"""
        return render_template('index.html')
    
    @app.route('/signup',  methods=['GET', 'POST'])
    def signup():
        """Sign up page: enables users to sign up"""
        #TODO: implement sign up logic here 
        error: str = None
        is_valid: bool = False
        if request.method == 'POST':
            try:
                user = Users(FirstName=request.form["FirstName"],
                            LastName=request.form["LastName"],
                            Email=request.form["Email"],
                            PhoneNumber=request.form["PhoneNumber"],
                            Password=request.form["Password"])
                if request.form["FirstName"].isalpha():
                    print(f'Input: {request.form["FirstName"]} is valid.')
                    if request.form["LastName"].isalpha():
                        print(f'Input: {request.form["LastName"]} is valid.')
                        if request.form["PhoneNumber"].isdigit() and len(request.form["PhoneNumber"]) == 10:
                            print(f'Input: {request.form["PhoneNumber"]} is valid.')
                            is_valid = True
                        else:
                            error_msg = f'Input: {request.form["PhoneNumber"]} is invalid! Phone Number must only contain 10 digits.'
                            print(f'Input: {request.form["PhoneNumber"]} is invalid!')
                            error = error_msg
                    else:
                        error_msg = f'Input: {request.form["LastName"]} is invalid! Last Name must only contain letters.'
                        print(f'Input: {request.form["LastName"]} is invalid!')
                else:
                    error_msg = f'Input: {request.form["FirstName"]} is invalid! First Name must only contain letters.'
                    print(f'Input: {request.form["FirstName"]} is invalid!')

                    error = error_msg
                if is_valid:
                    user_data: dict = {}
                    for key,value in request.form.items():
                        user_data[key] = value.strip()
                    passwordbytes = user_data["Password"].encode('utf-8')
                    hash = bcrypt.hashpw(passwordbytes, bcrypt.gensalt())
                    hashstore = hash.decode('utf-8')
                    hashed_user = Users(
                        FirstName=user_data["FirstName"],
                        LastName=user_data["LastName"],
                        Email=user_data["Email"],
                        PhoneNumber=user_data["PhoneNumber"],
                        Password=hashstore
                    )
                    insert_stmt = insert(hashed_user)


            except Exception as error:
                logger.error("Error inserting User", {error})
                user_error_msg = "Something went wrong on our end. Rest assured we are working to solve this problem. Please try again later."
                return render_template('error.html', error=user_error_msg)

        return render_template('signup.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Log in page: enables users to log in"""
        # TODO: implement login logic here
        if request.method == 'POST':
            try:
                user = get_one(Users, Email=request.form["Email"])
                if user:
                    triedpassword = request.form["Password"].strip().encode('utf-8')
                    storedpassword = user.Password.encode('utf-8')
                    if bcrypt.checkpw(triedpassword, storedpassword):
                        print("Login successful")
                        return redirect(url_for('success'))
                    else:
                        print("Incorrect password")
                        return redirect('/login')
                else:
                    print("No user exists with that email or password")
                    return redirect('/login')
                
            except Exception as error:
                print("Error finding User", {error})
                user_error_msg = "Something went wrong on our end. Rest assured we are working to solve this problem. Please try again later."
                return render_template('error.html', error=user_error_msg)
            
            
        return render_template('login.html')

    @app.route('/users')
    def users():
        """Users page: displays all users in the Users table"""
        all_users = get_all(Users)
        
        return render_template('users.html', users=all_users)

    @app.route('/success')
    def success():
        """Success page: displayed upon successful login"""

        return render_template('success.html')

    return app

if __name__ == "__main__":
    app = create_app()
    # debug refreshes your application with your new changes every time you save
    app.run(debug=True)