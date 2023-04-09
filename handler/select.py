from flask import Blueprint, request, jsonify, Flask, session, render_template, make_response
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from controller import select
import requests
from flask_restful import Resource
from flask.views import MethodView
from werkzeug.utils import secure_filename
from flask_swagger_ui import get_swaggerui_blueprint

# speeching module imports
import pyttsx3
import threading
import time

# jwt imports
import jwt
from jwt.algorithms import get_default_algorithms
from functools import wraps

# flask mail imports

from flask_mail import Mail, Message

bp = Blueprint('select', __name__, url_prefix="/select")

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisthesecretkey'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        print(app.config["SECRET_KEY"])
        print(token)
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        else:
            try:
                data = jwt.decode(token, app.config["SECRET_KEY"], get_default_algorithms())
            except Exception as error:
                print(error)
                return jsonify({'message': 'Token is invalid!'}), 403
            return f(*args, **kwargs)

    return decorated


@bp.route('/unprotected')
def unprotected():
    return jsonify({'message': 'Anyone can view this!'})


@bp.route('/protected')
@token_required
def protected():
    return jsonify({'message': 'This is only available for people with valid tokens.'})


@bp.route('/login')
def login():
    auth = request.authorization
    if auth and auth.password == 'secret':
        token = jwt.encode({'user': auth.username}, app.config['SECRET_KEY'])
        return jsonify({'token': token})
    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@bp.route('/', methods=(["GET", "POST"]))
@token_required
def select_records():
    return render_template("index.html", country_name=select.get_items_on_country())


@bp.route("/create", methods=(["GET", "POST"]))
@token_required
def get_records():
    return select.create_item()


@bp.route("/insert", methods=(["GET", "POST"]))
def insert_records():
    check = requests.get("https://apis.ccbp.in/countries-data")
    values = check.json()
    return str(select.insert_items_on_country(values))


@bp.route("/update", methods=(["GET", "POST"]))
def update_records():
    values = request.get_json()
    if select.update_item(values):
        engine.say("success fully updated")
        engine.runAndWait()
        return "success"
    else:
        return "failure"


@bp.route('/<username>', methods=(["GET", 'POST']))
def get_country(username):
    return str(select.country_name(username))


# random joke code
@bp.route('/createRandomJokeTable', methods=['GET', 'POST'])
def create_random_joke_table():
    if not "1050 (42S01): Table 'randomjoke' already exists" == select.create_randomJoke():
        return "successfully created"
    else:
        return "already created"


@bp.route('/randomJoke', methods=['GET', 'POST'])
def google():
    values = requests.get("https://apis.ccbp.in/jokes/random")
    value_content = values.json()
    if select.random_joke(value_content):
        return "successfully done"
    else:
        return "already stored please enter again 😂"


# Know Fact About the Number

@bp.route("/fact/<int:number>")
def fact_number(number):
    values = requests.get(f"https://apis.ccbp.in/numbers-fact?number={number}")
    return values.json()


@bp.route("/hello", methods=["GET", "POST"])
def func():
    return "hello naveen"


# login and registrations

auth = HTTPBasicAuth()


def get_data(email, password):
    users = select.get_item(email, password)
    if users:
        name = users[0]["name"]
        session[name] = users
        if (email == users[0]['email']) and check_password_hash(users[0]["password"], password):
            return users[0]["name"]
        else:
            return "please enter valid username and password"


@auth.verify_password
def verify_password(email, password):
    users = get_data(email, password)
    return users


@bp.route('/login', methods=(['GET', 'POST']))
@auth.login_required
def index():
    return "Hello, %s!" % auth.current_user()


@bp.route('/registration', methods=(['GET', 'POST']))
def registration():
    values = request.get_json()
    return select.registration(values)


@bp.route('/get', methods=['GET'])
def session_practice():
    return str(session.get('naveen', 'not set'))


# files uploading
@bp.route('/file', methods=['GET', 'POST'])
def file_template():
    return render_template('filesUpload.html')


@bp.route('/uploader', methods=['GET', 'POST'])
def files_upload():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'


def function_speech(value_content, fname):
    engine.say(f"hello {fname} listen my joke is" + value_content["value"])
    engine.startLoop()

    engine.runAndWait()


def function_value(value_content):
    pass
    # return value_content["value"]


@bp.route('/speechRandomJoke/<fname>')
def speech_random_joke(fname):
    values = requests.get("https://apis.ccbp.in/jokes/random")
    value_content = values.json()
    t2 = threading.Thread(target=function_speech, args=(value_content, fname))
    t1 = threading.Thread(target=function_value, args=(value_content,))
    t2.start()
    t1.start()
    # function_speech(value_content)
    engine.endLoop()
    engine.stop()
    return f"hello {fname} listen my joke " + str(value_content["value"])


# flask mail


mail_bp = Blueprint("mail", __name__, url_prefix="/mail")
# app = Flask(__name__)

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'billunaveen058@gmail.com'
app.config['MAIL_PASSWORD'] = '9959034250'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


# message object mapped to a particular URL ‘/’
@mail_bp.route("/")
def index():
    msg = Message(
        'hello',
        sender='billunaveen058@gmail.com',
        recipients=['billunaveen10@gmail.com']
    )
    msg.html = render_template('tourism.html')
    mail.send(msg)
    return render_template('tourism.html')
