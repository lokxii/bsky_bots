from flask import Flask, Blueprint

from app.chahan import chahan
from app.shuukei import shuukei

import gc


app = Flask(__name__)


@app.route("/")
def home():
    gc.collect()
    return "Hi"


index = Blueprint("index", __name__, url_prefix="/services")
index.register_blueprint(chahan)
index.register_blueprint(shuukei)

app.register_blueprint(index)
