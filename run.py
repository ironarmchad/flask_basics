from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config.update(


    SECRET_KEY="light57HOPE",
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:light57HOPE@localhost/catalog_db',
    SQLAlchemy_TRACK_NOTIFICATIONS=False
)

db = SQLAlchemy(app)

@app.route('/index')
@app.route('/')
def hello_world():
    return 'Hello Flask!'

@app.route('/new/')
def query_string(greeting = 'hello'):
    query_val = request.args.get('greeting', greeting)
    return '<h1> the greeting is : {0} </h1>'.format(query_val)

@app.route('/user')
@app.route('/user/<name>')
def no_query_string(name = 'mina'):
    return '<h1> hello there! {} </h1>'.format(name)


# Strings
@app.route('/text/<string:name>')
def working_with_strings(name):
    return '<h1> here is a string: ' + name + '</h1>'


# Integers
@app.route('/numbers/<int:num>')
def working_with_numbers(num):
    return '<h1>the number you picked is ' + str(num) + '</h1>'

@app.route('/add/<int:num1>/<int:num2>')
def adding_integers(num1, num2):
    return '<h1>the sum is: {}</h1>'.format(num1 + num2)

# FLOATS
@app.route('/product/<float:num1>/<float:num2>')
def product_two_numbers(num1, num2):
    return '<h1>the product is {}</h1>'.format(num1 * num2)

# USING TEMPLATES
@app.route('/temp')
def using_templates():
    return render_template("hello.html")

# Working with Jinja2 part 1
@app.route('/watch')
def top_movies():
    movie_list = ['autopsy of jane doe',
                  'neon demon',
                  'ghost in a shell'
                  'kong: skull island',
                  'john wick 2',
                  'spiderman - homecoming']

    return render_template('movies.html',
                           movies=movie_list,
                           name="Harry")

# Conditionals in Jinja2
@app.route('/tables')
def movies_plus():
    movies_dict = {'autopsy of jane doe': 2.14,
                  'neon demon': 3.20,
                  'ghost in a shell': 1.50,
                  'kong: skull island': 3.50,
                  'john wick': 2.52,
                  'spiderman - homecoming': 1.48}

    return render_template('table_data.html',
                           movies=movies_dict,
                           name='Sally')

# Filters in Jinja
@app.route('/filters')
def filter_data():
    movies_dict = {'autopsy of jane doe': 2.14,
                   'neon demon': 3.20,
                   'ghost in a shell': 1.50,
                   'kong: skull island': 3.50,
                   'john wick': 2.52,
                   'spiderman - homecoming': 1.48}

    return render_template('filter_data.html',
                           movies=movies_dict,
                           name=None,
                           film='a christmas carol')

# Macros in Jinja2
@app.route('/macros')
def jinja_macros():
    movies_dict = {'autopsy of jane doe': 2.14,
                   'neon demon': 3.20,
                   'ghost in a shell': 1.50,
                   'kong: skull island': 3.50,
                   'john wick': 2.52,
                   'spiderman - homecoming': 1.48}

    return render_template('using_macros.html', movies=movies_dict)

# Starting with DB
class Publication(db.Model):
    __tablename__ = 'publication'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Publisher is {}'.format(self.name)

class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())

    # Relationship
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id):
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.book_format = book_format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return '{} by {}'.format(self.title, self.author)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
