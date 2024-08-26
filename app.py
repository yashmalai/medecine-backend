from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint
from app import create_app
from app.extensions import db, migrate
#import os
#import dotenv


app = create_app()
#app.secret_key = "medecine"
#dotenv.load_dotenv()

#TODO перенести в коннфигурационный файл
#app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}" 
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


@app.route('/')
def index():
    return 'main'

'''
@app.route('/medicament')
def medicament():
    return render_template("medicament.html")

'''

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    #with app.test_request_context('/'):
        #print(app.full_dispatch_request().get_data(as_text=True))
    app.run(debug=True)
