from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
# from pymongo.objectid import ObjectId
from bson.objectid import ObjectId
import os

application = Flask(__name__)
application.config["MONGO_URI"] = os.environ.get("DATABASE_URL") + "/app?authSource=admin"
mongodb_client = PyMongo(application)
db = mongodb_client.db

@application.route("/")
def main():
    return render_template('index.html')

@application.route('/signUp',methods=['POST'])
def signUp():

    # read the posted values from the UI
    name = request.form['name']
    surname = request.form['surname']

    id = db.persons.insert_one({'name': name, 'surname': surname})
    print("ID is ", id)
    print("ID2 is ", id.inserted_id)

    return jsonify({"pid": str(id.inserted_id)})

@application.route('/view',methods=['POST'])
def view():
    pid = request.json['pid']
    print("The view pid: ", pid)

    p1 = db.persons.find_one({"_id": ObjectId(pid)})
    print("The p1 person: ", p1["name"])

    return jsonify({'name': p1["name"], 'surname': p1["surname"]})

if __name__ == "__main__":
    application.run()
