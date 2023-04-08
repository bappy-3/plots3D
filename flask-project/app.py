import time

from flask import Flask, render_template, request, flash
from sympy import *
import plotly.graph_objs as go
import numpy as np

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# Define the home page route
@app.route('/')
def home():
    return render_template('index.html')


# Define the plot route
@app.route('/plot', methods=['POST'])
def plot():
    # Get the equation from the form input
    expr_string = request.form['equation']

    # Define the variables
    x, y = symbols('x y')

    # Define the expression
    try:
        expr = sympify(expr_string)
    except SympifyError:
        flash("Invalid input, try again.")
        return render_template('error.html')
    except TypeError:
        return render_template('error.html')


    # Define the x and y ranges
    x_range = (-10, 10, 0.1)
    y_range = (-10, 10, 0.1)

    # Create a meshgrid from the ranges
    x_vals, y_vals = np.meshgrid(np.arange(*x_range), np.arange(*y_range))

    # Vectorize the expression
    vec_expr = lambdify((x, y), expr, 'numpy')

    # Calculate the z values
    z_vals = vec_expr(x_vals, y_vals)

    # Create the 3D surface plot
    fig = go.Figure(data=[go.Surface(x=x_vals, y=y_vals, z=z_vals)])
    plot_div = fig.to_html(full_html=False)

    # Render the output template
    return render_template('output.html', input_text=expr_string, plot_div=plot_div)

if __name__ == '__main__':
    app.run()

