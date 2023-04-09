from pandas import *
import numpy as np
from flask import Flask, render_template, request,Blueprint
import pickle

model = pickle.load(open("model.pkl", "rb"))

model_bp = Blueprint('moviePrediction', __name__, url_prefix="/moviePrediction")



@model_bp.route('/', methods=["GET", "POST"])
def movie_function():
    return render_template('linearRegression.html')


@model_bp.route("/predict", methods=["GET", "POST"])
def function_name():
     if request.method == "POST":
        budget_values = request.form.get('budget')
        if len(budget_values) == 0:
            return render_template('linearRegression.html',prediction_values="please enter values")
        else:
            budget = [iteration for iteration in budget_values]
            budget_int = int("".join(budget))
            numpy_budget = (np.array([budget_int])).reshape(-1, 1)
            convert_as_string_to_list = (model.predict(numpy_budget))[0]
            convert_as_string = [str(iteration) for iteration in convert_as_string_to_list]
            convert_as_float = ("".join(convert_as_string))
            convert_as_int = int(float(convert_as_float))
            return render_template('linearRegression.html',prediction_values=f"{convert_as_int}")


