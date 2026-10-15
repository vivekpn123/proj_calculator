from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/calculate")
def calculate():
    data = request.get_json(silent=True) or {}
    try:
        a, b = float(data.get("a")), float(data.get("b"))
        op = data.get("op")
    except (TypeError, ValueError):
        return jsonify(error="Enter two valid numbers."), 400

    if op == "add":
        result = a + b
    elif op == "subtract":
        result = a - b
    elif op == "multiply":
        result = a * b
    elif op == "divide":
        if b == 0:
            return jsonify(error="Cannot divide by zero."), 400
        result = a / b
    else:
        return jsonify(error="Unknown operation."), 400

    if result.is_integer():
        result = int(result)
    return jsonify(result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
