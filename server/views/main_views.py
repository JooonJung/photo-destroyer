from flask import Blueprint
from models import User
from flask import Response, request


bp = Blueprint('main', __name__, url_prefix='/api/v1/')

@bp.route('/signUp', methods = ["GET", "POST"])
def signUp():
    if request.method == "POST":    
        print(request.data)
        return Response(status=200)

if __name__ == "__main__":
    bp.run(debug = True)