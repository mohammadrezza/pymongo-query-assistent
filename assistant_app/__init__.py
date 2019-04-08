from flask import Flask
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/nobina"
mongo = PyMongo(app)


@app.route("/")
def main():
    return "it's working !"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, use_reloader=True, threaded=True)
