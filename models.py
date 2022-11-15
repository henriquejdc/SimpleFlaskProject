from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///livros.db'
db = SQLAlchemy(app)


class Autor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    sobrenome = db.Column(db.String(30), nullable=False)
    livros = db.relationship('Livro', backref='autor', lazy=True)

    def __repr__(self):
        return f'Autor("{self.nome}", "{self.sobrenome}")',


class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    sumario = db.Column(db.String(250), nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey('autor.id'), nullable=False)

    def __repr__(self):
        return f'Livro("{self.titulo}")'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(256))

    def __init__(self, body):
        self.body = body

    def __repr__(self):
        return "<Post({})>".format(self.id)
