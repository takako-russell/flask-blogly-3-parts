"""Blogly application."""

from flask import Flask,render_template,redirect,request,flash
from models import db,User,connect_db,Post


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'abdfasdfasdf'

connect_db(app)

app.app_context().push()
db.create_all()






@app.route("/")
def home():
    """Shows five most recent posts"""
   
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()

    return render_template("homepage.html" ,posts=posts)


@app.errorhandler(404)
def page_not_found(e):
    """Shows 404 error page"""

    return render_template('404.html'), 404


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

    flash("New user is added!")

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


@app.route("/users/<int:user_id>/posts/new", methods=['POST'])
def newpost(user_id):
    """Saves the new post in database"""

    user = User.query.get_or_404(user_id)
    
    newpost =  Post(title = request.form["new_title"],
    content = request.form["new_content"],user_id=user_id)

    db.session.add(newpost)
    db.session.commit()

    return redirect(f"/users/{user_id}")



@app.route("/users/<int:user_id>/posts/new")
def show_new_postform(user_id):
    """Shows a form to create a new post"""

    user = User.query.get_or_404(user_id)

    return render_template("new_postform.html",user=user)



@app.route("/users/<int:user_id>/posts/<int:post_id>")
def show_post(user_id, post_id):
    """Displays a post for a perticular post id """
    try:
        post = Post.query.get_or_404(post_id)


        return render_template("post.html",post=post)
    except Exception as e:
        print(e)
        return "internal Error,500"
    


@app.route("/users/<int:user_id>/posts/<int:post_id>/delete", methods=['POST'])
def delete_post(user_id,post_id):
    """Deletes post from the data base"""
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route("/users/<int:user_id>/posts/<int:post_id>/edit")
def edit_post(user_id,post_id):
    """Shows a form to edit a specific post"""

    post = Post.query.get_or_404(post_id)

    return render_template("post-edit.html",post=post)


@app.route("/users/<int:user_id>/posts/<int:post_id>/edit", methods=["POST"])
def update_editpost(user_id,post_id):
    """Saves the editted post in database"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form["edit-title"] 
    post.content = request.form["edit-content"]

    db.session.add(post)
    db.session.commit()

    return redirect (f"/users/{user_id}/posts/{post_id}")