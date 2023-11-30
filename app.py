"""Blogly application."""

from flask import Flask,render_template,redirect,request
from models import db,User,connect_db,Post


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'abdfasdfasdf'

connect_db(app)

app.app_context().push()
db.create_all()

@property
def fullname(self):
    """Returns a full name"""
    return f"{ self.first_name} { self.last_name }"


@app.route("/")
def home():
    """Redirects to a page with a list of users"""
   
    return redirect("/users")


@app.route("/users")
def users():
     """Shows users in html"""
     user_names =  User.query.order_by(User.first_name,User.last_name).all()

     return render_template("users.html",user_names = user_names)


@app.route("/users/<int:user_id>")
def userdetails(user_id):
    """Shows details of a user including a list of posts"""
    user = User.query.get_or_404(user_id)
    return render_template("details.html", user = user)


@app.route("/users/new", methods=["GET"])
def showform():
    """Shows a form to create a new post"""
    return render_template("form.html")


@app.route("/users/new", methods=["POST"])
def adduser():
    """Retrieves the new post from the form and updates the database"""

    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    imageURL = request.form["imageURL"]
   

    new_user = User(first_name = firstname, last_name = lastname, image_url = imageURL or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/edit" )
def show_edit(user_id):
    """Shows a form for the user to update his page"""
    user = User.query.get_or_404(user_id)

    return render_template("edit.html",user=user)



@app.route("/users/<int:user_id>/edit",methods=['POST'])
def edit(user_id):
    """Retrieves the eddited info from the form and updates the database"""
    user = User.query.get_or_404(user_id)

    user.first_name = request.form["edit_first_name"]
    user.last_name = request.form["edit_last_name"]
    user.image_url = request.form["edit_imageURL"]

    db.session.add(user)
    db.session.commit()

    return redirect("/users")



@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete(user_id):
    """Deletes the user from the database"""
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")



