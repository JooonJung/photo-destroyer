from flask import Blueprint
from models import User
import time

bp = Blueprint('main', __name__, url_prefix='/api/v1/')


@bp.route('/')
def main():
    return {
        "time" : time.time()
    }
if __name__ == "__main__":
    bp.run(debug = True)