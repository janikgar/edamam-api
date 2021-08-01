from flask import Flask, make_response
from flask_restx import Resource, Api
from edamam import get_upc, get_ingredient

def create_app(test_config=None) -> Flask:
    app = Flask(__name__)
    api = Api(app)

    @api.route( '/upc/<upc>')
    class Upc(Resource):
        def get(self, upc: str):
            return get_upc(upc)

    @api.route('/ingredient/<ingredient>')
    class Ingredient(Resource):
        def get(self, ingredient: str):
            return get_ingredient(ingredient)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)