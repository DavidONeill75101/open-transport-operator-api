from flask import Flask
from flask import request
from operators import Operators


app = Flask(__name__)
operator_util = Operators()


@app.route('/mode', methods=['GET'])
def mode():
    
    #return the list of all modes of transport
    maybe_modes = operator_util.get_modes()
    if maybe_modes is None:
        return "Failure", 400
    return maybe_modes, 200

    
@app.route('/operator', methods=['GET'])
def operator():
    #given the id, return the appropriate operator
    id = request.args.get('filterString')

    if id is None:
        #return all operators
        return 

    maybe_operator = operator_util.get_operator_by_id(id)
    if maybe_operator is None:
        return "Failure", 400
    return maybe_operator, 200
    