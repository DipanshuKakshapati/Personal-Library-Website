from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
# This line creates a new Flask application instance

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
# means that the database is located in the same directory as the application code and has a filename of books.db.
            
db = SQLAlchemy(app)
# creates a new SQLAlchemy instance and binds it to the Flask application instance                                                  



class Book(db.Model):
    '''
    This line defines a new database model called Book that inherits from the db.Model class provided by SQLAlchemy. 
    Book is a subclass of db.Model and will inherit all of the functionality provided by that class.
    '''
    id = db.Column(db.Integer, primary_key = True)                        
    # The column is of type db.Integer (meaning it will store integer values),
    # and is marked as the primary key for the table by setting primary_key=True.
    
    user_name = db.Column(db.String(50), nullable = False)               
    # The column is of type db.String(50) (meaning it will store string values up to 50 characters in length), 
    # and is marked as nullable=False (meaning it is required and cannot be left blank).   
                                                                  
    book_name = db.Column(db.String(100), nullable = False)

    author_name = db.Column(db.String(100), nullable = False)

    genre = db.Column(db.String(50), nullable = False)

    rating = db.Column(db.Integer, nullable = False)



@app.before_first_request
# registers a function to be executed before the first request to the Flask application
                                                
def create_tables():  
# this function executes before the first request to the Flask application.
                                                  
    db.create_all() 
    '''
    checks whether the table exists or not. 
    if does not exists creates the table.
    if exists then does not create a new table.
    '''



@app.route('/')
# creates a new route for the Flask application.
# When a user navigates to the http://localhost:5000/, the login() function will be executed.

def login():
    # this function will be executed when a user navigates to the http://localhost:5000/ of the Flask application 
                                                               
    return render_template('login.html')
    # the login.html template will be rendered and returned as a response to the user's request. 

                              

@app.route('/login', methods=['POST'])     
# creates a new route for the Flask application.
# The methods parameter is set to ['POST'], which means that this route will only accept HTTP POST requests.  
                         
def admin_check():                                                      
    # this function will be executed when a user submits a form with HTTP POST method to the /login URL

    admin_name = request.form.get('username')
    # retrieves the value of the username form field that was submitted in the HTTP POST request.
                               
    admin_password = request.form.get('password')
    # retrieves the value of the password form field that was submitted in the HTTP POST request.

    if admin_name == 'Admin' and admin_password == '@dm1n':
    # if the admin_name and admin_password variables match the values for the admin user account.              
        return redirect('/library')
    # the user is redirected to the /library URL

    elif admin_name == 'User' and admin_password == 'Us3r':
    # if the admin_name and admin_password variables match the values for the user account. 
        return redirect('/add_books')
    # the user is redirected to the /add_books URL

    else:    
        return render_template('login.html')
    # if neither the admin nor user credentials match. If this is the case, the user is returned to the login.html template 


    
@app.route('/add_books')
# creates a new route for the Flask application.
                                                
def addmore():  
 # this function will be executed when a user navigates to the /add_books URL of the Flask application.    
                                                    
    return render_template('friend_entry.html')   
     # the friend_entry.html template will be rendered and returned as a response to the user's request.         



@app.route('/library')   
# creates a new route for the Flask application.
                                              
def library():
# this function will be executed when a user navigates to the /library URL of the Flask application.
                                                         
    users = Book.query.all()       
    # The query.all() method is used to retrieve all the rows from the table, and the results are stored in the users variable.
                                         
    return render_template('book.html',users=users)
'''
the book.html template will be rendered and returned as a response to the user's request.
The users variable is passed as a parameter to the template, so that the template can display the book records in the table. 
'''



@app.route('/books', methods=['POST'])                                  
# creates a new route for the Flask application.  
# The methods parameter is set to ['POST'], which means that this route will only accept HTTP POST requests. 
                                                                    
def index():
    # this function will be executed when a user submits a form with HTTP POST method to the /books URL
                                                              
    user_name = request.form['user_name']
    # retrieves the value of the user_name form field that was submitted in the HTTP POST request.    
                             
    book_name = request.form['book_name']                                
    # retrieves the value of the book_name form field that was submitted in the HTTP POST request.

    author_name = request.form['author_name']                            
    # retrieves the value of the author_name form field that was submitted in the HTTP POST request.

    genre = request.form['genre']                                        
    # retrieves the value of the genre form field that was submitted in the HTTP POST request.

    rating = request.form['rating']                                      
    # retrieves the value of the rating form field that was submitted in the HTTP POST request.

    user = Book(user_name=user_name, book_name=book_name, author_name=author_name, genre=genre, rating=rating)
    # creates a new Book object using the values submitted in the HTTP POST request. The Book object is initialized with the values of user_name, book_name, author_name, genre, and rating.

    db.session.add(user)
    #  adds the new Book object to the SQLAlchemy session so that it can be saved to the database.

    db.session.commit()
    # commits the changes made to the SQLAlchemy session to the database.

    users = Book.query.all()
    # The query.all() method is used to retrieve all the rows from the table, and the results are stored in the users variable.

    return redirect('/thank_you') 
    # returns a redirect response to the user's request.



@app.route('/thank_you') 
# creates a new route for the Flask application.

def thank_you():
# this function will be executed when a user navigates to the /thank_you URL of the Flask application.

    return render_template('thank_you.html') 
    # the thank_you.html template will be rendered and returned as a response to the user's request.



@app.route('/delete/<int:id>') 
# creates a new route for the Flask application.
# The <int:id> portion of the URL is a dynamic route parameter that allows Flask to capture an integer value from the URL and pass it as an argument to the delete() function.

def delete(id): 
# this function will be executed when a user navigates to the /delete/<int:id> URL of the Flask application.

    user_to_delete = Book.query.get_or_404(id) 
    # retrieves the book record with the id value passed as a parameter to the delete() function.
    # If no record is found with the specified id, a 404 error page is displayed to the user

    try:
        # attempts to delete the user_to_delete object from the SQLAlchemy session and commit the changes to the database.

        db.session.delete(user_to_delete)  

        db.session.commit()

        return redirect('/library')
        # If the deletion is successful, the user is redirected to the /library URL
    
    except:
        return "There was a problem deleting that user...." 
        #  If the deletion is unsuccessful, an error message is displayed to the user. 



@app.route('/search', methods=['POST']) 
# creates a new route for the Flask application.
# The methods parameter is set to ['POST'], which means that this route will only accept HTTP POST requests.

def search():                           
# This function will be executed when a user submits a form with HTTP POST method to the /search URL

    user_name = request.form.get('user_name') 
    # retrieves the value of the user_name form field that was submitted in the HTTP POST request.

    users = Book.query.filter_by(user_name=user_name).all() 
    #  retrieves all the rows from the Book table in the SQLite database that have the same user_name value as the user_name form field that was submitted in the HTTP POST request. 
    # query.filter_by() method is used to filter the rows based on the user_name column, and the results are stored in the users variable.

    return render_template('book_search.html', users=users) 
    # the book_search.html template will be rendered and returned as a response to the user's request.
    # The users variable is passed as a parameter to the template, so that the template can display the book records in the table. 



if __name__ == '__main__': 
    # condition checks whether the script is being run directly by the Python interpreter

    app.run(debug=True) 
    # method is called to start the Flask application with the debug mode enabled.