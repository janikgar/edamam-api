import os
from flask import Flask, make_response, Config
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
    
    load_dotenv()
    return app
