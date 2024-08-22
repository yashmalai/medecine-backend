from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    name = input("What is your name? ")
    print(f"Hello, {name}")
    return "Checked"

if __name__ == '__main__':
    with app.test_request_context('/'):
        print(app.full_dispatch_request().get_data(as_text=True))
    app.run(debug=True)
