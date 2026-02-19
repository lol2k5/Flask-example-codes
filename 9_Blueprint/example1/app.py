from flask import Flask
from simple_blueprint_example import simple_example


app = Flask(__name__)
app.register_blueprint(simple_example)

# flask --app app.py run