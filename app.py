from flask import Flask, make_response
from flask_restx import Resource, Api
from edamam import get_upc

app = Flask(__name__)
api = Api(app)

@api.route( '/upc/<upc>')
class Upc(Resource):
    def get(self, upc: str):
        return get_upc(upc)

if __name__ == "__main__":
    app.run(debug=True)