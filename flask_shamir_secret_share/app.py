import random
from math import ceil
from decimal import Decimal
from flask import Flask, request, render_template

app = Flask(__name__)

FIELD_SIZE = 10**5

def reconstruct_secret(shares):
    total_sum = 0

    for j, (xj, yj) in enumerate(shares):
        prod = Decimal(1)

        for i, (xi, _) in enumerate(shares):
            if i != j:
                prod *= Decimal(xi) / Decimal(xi - xj)

        prod *= Decimal(yj)
        total_sum += prod

    return int(total_sum)

def polynomial_value(x, coefficients):
    evaluation_point = 0
    for coefficient_index, coefficient_value in enumerate(coefficients[::-1]):
        evaluation_point += x ** coefficient_index * coefficient_value
    return evaluation_point

def generate_coefficients(threshold, secret):
    coefficients = [random.randrange(0, FIELD_SIZE) for _ in range(threshold - 1)]
    coefficients.append(secret)
    return coefficients

def generate_shares(total_shares, threshold, secret):
    coefficients = generate_coefficients(threshold, secret)
    shares = []

    for _ in range(1, total_shares + 1):
        x = random.randrange(1, FIELD_SIZE)
        shares.append((x, polynomial_value(x, coefficients)))

    return shares

@app.route("/", methods=["GET", "POST"])
def index():
    threshold = 3  # Set threshold to 3
    total_shares = 5  # Set total shares to 5

    if request.method == "POST":
        secret = int(request.form["secret"])

        # Part 1: Generation of shares
        shares = generate_shares(total_shares, threshold, secret)

        return render_template("index.html", shares=shares, threshold=threshold)

    return render_template("index.html", shares=[], threshold=threshold)

@app.route("/recover", methods=["POST"])
def recover():
    threshold = 3  # Set threshold to 3

    selected_shares = []

    for i in range(1, threshold + 1):
        x = int(request.form[f"x_{i}"])
        y = int(request.form[f"y_{i}"])
        selected_shares.append((x, y))

    # Part 2: Secret Reconstruction
    reconstructed_secret = reconstruct_secret(selected_shares)

    return f"Reconstructed Secret: {reconstructed_secret}"

if __name__ == '__main__':
    app.run()
