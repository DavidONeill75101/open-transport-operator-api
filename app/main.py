from flask import Flask
from flask import request

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from operators import Operators

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

operator_util = Operators()


@app.route("/mode", methods=["GET"])
@limiter.limit("1 per second")
def mode():
    """mode query returns json representing all modes available or an error if unsuccessful
    """

    maybe_modes = operator_util.get_modes()
    if maybe_modes is None:
        return "Error Occurred", 400
    return maybe_modes, 200


@app.route("/operator", methods=["GET"])
@limiter.limit("1 per second")
def operator():
    """operator query returns json representing operators or an error if unsuccessful
    optional parameter filterString can be used to pass in id of operator to fetch
    """
    id = request.args.get("filterString")
        
    maybe_operator = operator_util.get_operator_by_id(id)
    if maybe_operator is None:
        return "Error occurred", 400
    return maybe_operator, 200


if __name__ == "__main__":
    app.run(debug=True)
    