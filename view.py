from flask import Flask
from handler import select
from flask_session import Session
from linearRegression import view

from flask_mail import Mail

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.register_blueprint(select.bp)
app.register_blueprint(view.model_bp)
app.register_blueprint(select.mail_bp)


if __name__ == '__main__':
    app.run(debug=True)

# importing libraries
