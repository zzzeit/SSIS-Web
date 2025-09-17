from flask import Flask

# 2. Create an instance of the Flask class
app = Flask(__name__)

# 3. Define a route and a function to run when the route is accessed
@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/test")
def test():
    return "Test"

# This part is optional but good practice to run the app
if __name__ == "__main__":
    app.run(debug=True)