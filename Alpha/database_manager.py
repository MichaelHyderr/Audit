from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789'

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///audit.db'
db = SQLAlchemy()
db.init_app(app)


# CREATE TABLES IN DB
class User(UserMixin, db.Model):
    __tablename__ = "users_table"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    answers = db.relationship("Answer", back_populates="author")


class Question(db.Model):
    __tablename__ = "questions_table"
    id = db.Column(db.Integer, primary_key=True)
    kss = db.Column(db.String(50))
    ksa = db.Column(db.String(50))
    description = db.Column(db.String(200))


class Answer(db.Model):
    __tablename__ = "answers_table"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users_table.id"))
    author = db.relationship("User", back_populates="answers")
    question_id = db.Column(db.Integer, db.ForeignKey("questions_table.id"))
    question = db.relationship("Question")
    value = db.Column(db.Integer)


with app.app_context():
    db.create_all()


def ksss_list():
    with app.app_context():
        ksss = db.session.query(Question.kss).distinct().all()  # Ci sono più righe con lo stesso kss quindi uso distinct()
        ksss = [kss[0] for kss in ksss]
        return ksss


def ksas_list(kss):
    with app.app_context():
        ksas = db.session.query(Question.ksa).where(Question.kss == kss).distinct().all()  # .all() fa ritornare una lista dei risultati
        ksas = [ksa[0] for ksa in ksas]  # [0] perchè la lista sopra è cosi' ([kss,], [kss2,],...)
        return ksas


def questions_list(ksa):
    with app.app_context():
        questions = db.session.query(Question.description).where(Question.ksa == ksa)
        questions = [question[0] for question in questions]
        questions_and_ids = [
            [question, db.session.execute(db.select(Question).where(Question.description == question)).scalar().id] for
            question in questions] # creo una lista di liste da passare all'html così [[question, id], [question2, id],...]
        return questions_and_ids


def record_exists(author_id, question_id):
    with app.app_context():
        existing_record = db.session.query(Answer).filter_by(author_id=author_id, question_id=question_id).first()  # cerco se esiste in Answer una riga con quei filtri presenti
        return existing_record is not None  # la riga sopra da come risultato la riga se esiste oppure None
                                            # quindi scrivo "is not None" così se non è None e quindi esiste il return da True
                                            # mentre se è il contrario da False

def user_results(user_id):
    with app.app_context():
        user = db.session.query(User).filter_by(id=user_id).first()
        answers = user.answers
        answers_list = []
        for a in answers:
            answers_list.append(a.value)
        return answers_list



# ---- SCRIVO LE DOMANDE SUL DB TABELLA QUESTION ----
# dal csv

# df = pd.read_csv("questions.csv")
# n = 0
# for _, row in df.iterrows():
#     n += 1
#     with app.app_context():
#         new_record = Question(id=n, kss=row["kss"], ksa=row["ksa"], description=row["description"])
#         db.session.add(new_record)
#         db.session.commit()
