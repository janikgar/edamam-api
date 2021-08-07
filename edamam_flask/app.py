import os
import json
from flask import Flask, make_response, Config, render_template
from flask.cli import load_dotenv
from flask_restx import Resource, Api
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource as TraceResource
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter  
from edamam_flask.edamam import get_upc, get_ingredient

nutrient_map = {
    'CA': {
        'name': 'Calcium',
        'unit': 'mg',
    },
    'CHOCDF': {
        'name': 'Carbohydrates',
        'unit': 'g',
    },
    'CHOLE': {
        'name': 'Cholesterol',
        'unit': 'mg',
    },
    'FAMS': {
        'name': 'Monounsaturated Fat',
        'unit': 'g',
    },
    'FAPU': {
        'name': 'Polyunsaturated Fat',
        'unit': 'g',
    },
    'FASAT': {
        'name': 'Saturated Fat',
        'unit': 'g',
    },
    'FAT': {
        'name': 'Fat',
        'unit': 'g',
    },
    'FATRN': {
        'name': 'Trans Fat',
        'unit': 'g',
    },
    'FE': {
        'name': 'Iron',
        'unit': 'mg'
    },
    'FIBTG': {
        'name': 'Fiber',
        'unit': 'g',
    },
    'FOLDFE': {
        'name': 'Folate',
        'unit': 'mcg',
    },
    'K': {
        'name': 'Potassium',
        'unit': 'mg',
    },
    'MG': {
        'name': 'Magnesium',
        'unit': 'mg',
    },
    'NA': {
        'name': 'Sodium',
        'unit': 'mg',
    },
    'ENERC_KCAL': {
        'name': 'Calories',
        'unit': 'kcal',
    },
    'NIA': {
        'name': 'Niacin',
        'unit': 'mg',
    },
    'P': {
        'name': 'Phosphorus',
        'unit': 'mg',
    },
    'PROCNT': {
        'name': 'Protein',
        'unit': 'g',
    },
    'RIBF': {
        'name': 'Riboflavin',
        'unit': 'mg',
    },
    'SUGAR': {
        'name': 'Sugar',
        'unit': 'g',
    },
    'THIA': {
        'name': 'Thiamin',
        'unit': 'mg',
    },
    'TOCPHA': {
        'name': 'Vitamin E',
        'unit': 'mg',
    },
    'VITA_RAE': {
        'name': 'Vitamin A',
        'unit': 'mcg',
    },
    'VITB12': {
        'name': 'Vitamin B12',
        'unit': 'mcg',
    },
    'VITB6A': {
        'name': 'Vitamin B6',
        'unit': 'mg',
    },
    'VITC': {
        'name': 'Vitamin C',
        'unit': 'mg',
    },
    'VITD': {
        'name': 'Vitamin D',
        'unit': 'mcg',
    },
    'VITK1': {
        'name': 'Vitamin K',
        'unit': 'mcg',
    }
}

def create_app(test_config=None) -> Flask:
    app = Flask(__name__)
    app.config['EDAMAM_FOOD_APP_IP'] = os.getenv('EDAMAM_FOOD_APP_IP', '00000000')
    app.config['EDAMAM_FOOD_APP_IP_KEY'] = os.getenv('EDAMAM_FOOD_APP_IP_KEY', '00000000000000000000000000000000')
    app.config['TRACE_HOST'] = os.getenv('TRACE_HOST', 'localhost')
    app.config['TRACE_PORT'] = os.getenv('TRACE_PORT', '6831')
    trace.set_tracer_provider(TracerProvider(
        resource=TraceResource.create({'service.name':'edamam_flask'})
    ))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(JaegerExporter(
            agent_host_name=app.config['TRACE_HOST'],
            agent_port=int(app.config['TRACE_PORT']),
        ))
    )
    FlaskInstrumentor().instrument_app(app)
    RequestsInstrumentor().instrument()
    tracer = trace.get_tracer_provider().get_tracer(__name__)
    api = Api(app)

    @api.route('/upc/<upc>')
    class Upc(Resource):
        def get(self, upc: str):
            return get_upc(upc)

    @api.route('/ingredient/<ingredient>')
    class Ingredient(Resource):
        def get(self, ingredient: str):
            return get_ingredient(ingredient)
    
    @app.route('/render/upc/<upc>')
    def render_upc(upc: str):
        upc_data = get_upc(upc)
        upc_data_content = upc_data.json
        food_data = upc_data_content['content']['hints'][0]['food']
        print(food_data)
        title = food_data['label']
        image = food_data['image']
        nutrients = food_data['nutrients']
        serving_sizes = food_data['servingSizes']
        servings_per_container = food_data['servingsPerContainer']
        upc_text = format(int(upc), '012')
        return render_template(
            'render.html',
            title=title,
            upc=upc_text,
            image=image,
            nutrients=nutrients,
            nutrient_map=nutrient_map,
            serving_sizes=serving_sizes,
            servings_per_container=servings_per_container,
            )

    load_dotenv()
    return app
