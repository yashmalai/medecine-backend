import click
from flask import Flask, request, jsonify

app = Flask(__name__)

# Декоратор для создания консольной команды
@click.group()
def cli():
    pass

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello, World!"

# Превращение маршрута в консольную команду
@cli.command()
def hello_console():
    print(hello())

@app.route('/echo', methods=['POST'])
def echo():
    data = request.json
    return jsonify(data)

# Превращение маршрута в консольную команду
@cli.command()
@click.option('--data', prompt='Data to echo', help='JSON data to echo back')
def echo_console(data):
    with app.test_request_context(json=data):
        print(echo().get_data(as_text=True))

if __name__ == '__main__':
    cli()
