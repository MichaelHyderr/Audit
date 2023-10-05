from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, URL
from database_manager import ksss_list, ksas_list, questions_list, User, Question, Answer, record_exists

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789'  # obbligatoria

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///audit.db'
db = SQLAlchemy()
db.init_app(app)  # Collego il db a Flask

# INITIALIZE LOGIN MANAGER
login_manager = LoginManager()
login_manager.init_app(app)  # Collego il login-manager a Flask


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


@app.route('/')
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)  # current_user.is_authenticated da come risultato True o False


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form
        result = db.session.execute(db.select(User).where(User.email == data["email"]))  # verifico che quel valore email è già presente in db
        user = result.scalar()
        if user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))
        new_user = User(email=data["email"],
                        password=generate_password_hash(data["password"], method='pbkdf2:sha256', salt_length=8),
                        name=data["name"])
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("welcome"))
    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        email = data["email"]
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, data["password"]):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('welcome'))
    return render_template("login.html", logged_in=current_user.is_authenticated)


@app.route('/welcome')
@login_required
def welcome():
    return render_template("welcome.html", name=current_user.name, logged_in=True)


# questions = questions_json()


@app.route("/survey", methods=["GET", "POST"])
@login_required
def survey():
    if request.method == "POST":
        data = request.form
        result = list(data.items())  # data è una ImmutableMultiDict (è un radio form(scelta multipla)), per estrapolare i risultati devo scrivere così
        for answer in result:  # sull'html ho fatto in modo che il risultato includa l'id della domanda e il valore della risposta in una lista di liste [[id, risultato], [31, 2], [32, 3]....]
            q_id = int(answer[0])
            question_answered = db.get_or_404(Question, q_id)  # Cerco la riga corrispondente all'id della domanda sulla tabella Questions
            answer = Answer(value=int(answer[1]), author=current_user, question=question_answered)
            if not record_exists(author_id=current_user.id, question_id=q_id):
                db.session.add(answer)
                db.session.commit()
                flash("Submission Successful")
            else:
                flash("You've already answered those questions!")
                return redirect(url_for("survey"))
    return render_template("survey.html", logged_in=True, ksss=ksss_list(), questions=questions_list, ksas_list=ksas_list)
    # ksss_list() la lancio qui al contrario delle altre due che invece mi conviene lanciarle nell'html perchè hanno bisogno degli arguments che produce ksss


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
