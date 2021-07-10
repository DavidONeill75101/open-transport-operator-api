from flask import Flask
from flask import request
from flask import render_template

import json

from operators import Operators

application = Flask(__name__)

operator_util = Operators()


@application.route("/", methods=["GET"])
def root():
    """return rot page
    """

    return "Open Transport Operator-info API"

       
@application.route("/mode", methods=["GET"])
def mode():
    """mode query returns json representing all modes available or an error if unsuccessful
    """

    maybe_modes = operator_util.get_modes()
    if maybe_modes is None:
        return "Error", 400
        
    return json.dumps(maybe_modes), 200
    

@application.route("/operator", methods=["GET"])
def operator():
    """operator query returns json representing operators or an error if unsuccessful
    optional parameter filterString can be used to pass in id of operator to fetch
    """
    id = request.args.get("filterString")
        
    maybe_operator = operator_util.get_operator_by_id(id)
    if maybe_operator is None:
        return "Error", 400
        
    return json.dumps(maybe_operator), 200
    

if __name__ == "__main__":
    application.run()
    