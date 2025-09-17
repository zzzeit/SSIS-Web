from flask import Flask, jsonify
from flask_cors import CORS
import database.data_management as dm

# 2. Create an instance of the Flask class
app = Flask(__name__)
CORS(app)
# 3. Define a route and a function to run when the route is accessed
@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/get/students")
def test():
    DM = dm.DataManager()
    return jsonify(DM.get_students())

@app.route("/get/students/<int:id>")
def getStudentById(id):
    DM = dm.DataManager()
    return jsonify(DM.get_student_by_id(id))

# This part is optional but good practice to run the app
if __name__ == "__main__":
    app.run(debug=True)