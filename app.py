from flask import Flask, request, jsonify
from databasemanager import DatabaseManager

app = Flask(__name__)

database_context = DatabaseManager("teste")

if __name__ == "__main__":
    app.run(debug=True)