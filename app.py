from flask import Flask, render_template, redirect, session, flash
from models import connect_db, db, User, Paragraph, Image
from forms import UserRegistrationForm, UserLoginForm, ParagraphForm, SearchDateForm
import requests
import datetime
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL', 'postgres:///paragraph_db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ['SECRET_KEY']

client_id = os.environ['ACCESS_KEY']

connect_db(app)

def get_image():
    """Check to see whether there's already an image in the database for today
#     If so return that image, otherwise call the Unsplah API, create a new image, and return that"""
#     image = Image.query.filter(date_added == datetime.date.today()
    response = requests.get(f"http://api.unsplash.com/photos/random?content_filter=high&client_id={client_id}")
    today_image = Image.query.filter(Image.date_added == datetime.date.today()).first()
    if today_image:
        return today_image
    else:
        new_image = Image(image_url=response.json()['urls']['thumb'], photographer=response.json()['user']['name'], credit_url = response.json()['user']['links']['html'])
        db.session.add(new_image)
        db.session.commit()
        new_today_image = Image.query.filter(Image.date_added == datetime.date.today()).first()
        return new_today_image

@app.route('/')
def home_page():
    """Display homepage for visitor, not logged in"""
    if "user_id" in session:
        return redirect(f"/users/{session['user_id']}")

    return render_template("home.html")

@app.route('/about')
def about_page():
    """Display "About" page for visitor, not logged in"""
    if "user_id" in session:
        return redirect(f"/users/{session['user_id']}")

    return render_template("about.html")

@app.route('/register', methods=["GET", "POST"])
def register_user():
    """Display registration form if noone is logged in, add new user to database.
    If username or email is already used, rerender form and provide error message"""
    if "user_id" in session:
        return redirect(f"/users/{session['user_id']}")

    form = UserRegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        used_email = User.query.filter(User.email==email).first()
        if used_email:
            form.email.errors = ["Email address has already been used"]

        used_username = User.query.filter(User.username==username).first()
        if used_username:
            form.username.errors = ["Username has already been used"]

        if not used_email and not used_username:
            if email == "":
                new_user = User.register(username, password)
            else:
                new_user = User.register(username, password, email)
            db.session.add(new_user)
            db.session.commit()
            new_user_id = User.query.filter_by(username=username).first().id
            session['user_id'] = new_user_id
            return redirect(f'/users/{new_user_id}')

    return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login_user():
    """Render login form. If user is already logged in redirect to user view, otherwise 
    provide error message on form"""
    if "user_id" in session:
        return redirect(f"/users/{session['user_id']}")
    
    form = UserLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            session['user_id'] = user.id
            return redirect(f'/users/{user.id}')
        elif User.query.filter(User.username==username).first():
            form.password.errors = ["Invalid password"]
        else:
            form.username.errors = ["Invalid username"]

    return render_template('login.html', form=form)

@app.route('/<int:user_id>/logout')
def logout_user(user_id):
    """Remove current user id from the session"""
    if session['user_id'] == user_id:
        session.pop('user_id')
    return redirect('/')

@app.route('/users/<int:user_id>', methods=["GET", "POST"])
def user_home(user_id):
    """Render home view for logged in user, show today's image, provide form for submitting paragraph.
    On submit, add paragraph to database and redirect to user's "My Paragraphs" page"""
    if "user_id" not in session:
        flash("You must login to create a paragraph")
        return redirect('/')
    
    if session['user_id'] != user_id:
        flash("You may not create a paragraph for another user")
        return redirect('/')

    user = User.query.get_or_404(user_id)
    image = get_image()
    form = ParagraphForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        public = form.public.data
        new_paragraph = Paragraph(title=title, content=content, public=public, user_id=user_id, image_id=image.id)
        db.session.add(new_paragraph)
        db.session.commit()
        return redirect(f'/users/{user_id}/paragraphs')
    
    return render_template('user_view.html', user=user, image=image, form=form)

@app.route('/users/<int:user_id>/paragraphs')
def view_user_paragraphs(user_id):
    """Render view of user's saved paragraphs"""

    if "user_id" not in session:
        flash("You must login to view your paragraphs")
        return redirect('/')

    if session['user_id'] != user_id:
        flash("You may not view another user's private paragraphs")
        return redirect('/')
    
    paragraphs = Paragraph.query.filter(Paragraph.user_id==user_id).order_by(Paragraph.id.desc()).all()

    return render_template("user_paragraphs.html", paragraphs=paragraphs, user_id=user_id)

@app.route('/public_paragraphs', methods=["GET", "POST"])
def view_public_paragraphs():
    """Provide logged in user with view of others' recent paragraphs"""

    if "user_id" not in session:
        flash("You must login to view public paragraphs")
        return redirect('/')
    
    paragraphs = Paragraph.query.filter(Paragraph.public==True).order_by(Paragraph.id.desc()).limit(10).all()
    form = SearchDateForm()
    if form.validate_on_submit():
        image_exists = Image.query.filter(Image.date_added==form.date.data).first()
        if image_exists:
            paragraphs_exist = Paragraph.query.filter(Paragraph.image_id==image_exists.id).order_by(Paragraph.id.desc()).limit(10).all()
            if paragraphs_exist:
                paragraphs = paragraphs_exist
            else:
                form.date.errors = ["No paragraphs were submitted on that date"]
        else:
            form.date.errors = ["No paragraphs were submitted on that date"]
    
    return render_template('public_paragraphs.html', paragraphs=paragraphs, user_id=session['user_id'], form=form)

@app.route('/edit_paragraph/<int:paragraph_id>', methods=["GET", "POST"])
def edit_paragraph(paragraph_id):
    """Render form for user to edit a paragraph and process form submission"""

    if "user_id" not in session:
        flash("You must login to edit paragraphs")
        return redirect('/')

    paragraph = Paragraph.query.get_or_404(paragraph_id)
    if session['user_id'] != paragraph.user_id: 
        flash("You may not edit another user's paragraph")
        return redirect('/')  

    form = ParagraphForm(obj=paragraph)
    if form.validate_on_submit():
        paragraph.title = form.title.data
        paragraph.content = form.content.data
        paragraph.public = form.public.data
        db.session.commit()
        return redirect(f'/users/{paragraph.user_id}/paragraphs')

    return render_template("paragraph_edit.html", paragraph=paragraph, form=form)

@app.route('/delete_paragraph/<int:paragraph_id>', methods=["POST"])
def delete_paragraph(paragraph_id):
    """Delete a logged in user's paragraph from the database"""

    if "user_id" not in session:
        flash("You may not delete another user's paragraph")
        return redirect('/')

    paragraph = Paragraph.query.get_or_404(paragraph_id)
    if session['user_id'] != paragraph.user_id: 
        flash("You may not delete another user's paragraph")
        return redirect('/')  
    
    db.session.delete(paragraph)
    db.session.commit()

    return redirect(f'/users/{paragraph.user_id}/paragraphs')





