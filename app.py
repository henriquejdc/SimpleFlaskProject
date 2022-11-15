from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    url_for,
    abort,
    make_response
)
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from models import db
import jsonify

app = Flask(__name__)

app.config['SECRET_KEY'] = 'chavesecreta'

with app.app_context():
    db.init_app(app)


class LivroForm(FlaskForm):
    titulo = StringField('Titulo do Livro', validators=[DataRequired()])
    autor = StringField('Nome do Autor', validators=[DataRequired()])
    vivo = BooleanField('Autor está Vivo?')
    genero = SelectField(
        'Gênero:',
        choices=[
            ('aventura', 'Aventura'),
            ('cientifico', 'Cientifico'),
            ('romance', 'Romance')
        ]
    )
    resumo = TextAreaField()
    submit = SubmitField('Enviar')


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/index/')
def index():
    nome = 'Henrique'
    return render_template('index.html', nome=nome)


@app.route('/jinja/')
def jinja():

    num = 10
    online = True
    langs = ['Python', 'Javascript', 'C', 'C++', 'Bash', 'Haskell']
    cores = ('red', 'green', 'blue')
    personagens = {
        'DBZ': 'Goku',
        'Naruto': 'Kakashi',
        'Death Note': 'Raito Yagami',
        'Akira': 'Tetsuo',
        'Pokémon': 'Ash'
    }

    class Aplicacao:
        def __init__(self, nome, descricao, url):
            self.nome = nome
            self.descricao = descricao
            self.url = url

        def nome(self):
            return f'O nome da aplicação é {self.nome}'

        def endereco(self):
            return f'Você pode acessar a aplicação atraves do endereço: {self.url}'

    appplication = Aplicacao(
        nome='Flask Prog. Web', descricao='Tutorial', url='github.com/henriquejdc'
    )

    def cubo(x):
        return x**3

    html = '<h1>Titulo</h1>'

    hacked = "<script>alert('Hackeado')</script>"

    return render_template(
        'jinja.html',
        num=num,
        langs=langs,
        personagens=personagens,
        cores=cores,
        online=online,
        Aplicacao=Aplicacao,
        cubo=cubo,
        app=appplication,
        html=html,
        hacked=hacked
    )


@app.route('/static/')
def arquivos_static():
    return render_template('static.html')


@app.route('/formulario/', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        req = request.form

        nome = req['nome']
        email = req.get('email')
        senha = request.form['senha']

        print(nome, email, senha)

        return redirect(request.url)

    return render_template('formulario.html')


@app.route('/wtf/', methods=['GET', 'POST'])
def wtf():
    form = LivroForm()
    if form.validate_on_submit():
        session['titulo'] = form.titulo.data
        session['autor'] = form.autor.data
        session['vivo'] = form.vivo.data
        session['genero'] = form.genero.data
        session['resumo'] = form.resumo.data

        return redirect(url_for('obrigado'))

    return render_template('wtf.html', form=form)


@app.route('/obrigado/')
def obrigado():
    return render_template('obrigado.html')


@app.route('/arquivojson/')
def arquivojson():
    lista = [1, 2, 3, 4, 5]
    dict = {'números': lista, 'nome': 'Números'}

    return jsonify({'output': dict})


@app.route('/abort/')
def abort():
    abort(404)  # Retorna o erro 404
    render_template('index.html')  # Essa linha nunca é executada


@app.route('/cookie/')
def cookie():
    resposta = make_response(render_template('index.html'))
    resposta.set_cookie('nome_do_cookie', 'valor_do_cookie')
    return resposta


@app.route('/session/')  # Seta a sessão
def session():
    session['nome_da_chave'] = 'valor_da_chave'  # Guarda um cookie seguro no browser
    return redirect(url_for('index'))


if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
    # app.run(host='0.0.0.0')
    # app.run(port=3535)
