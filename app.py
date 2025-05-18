from flask import Flask
from flask_restx import Api
from api.health import health_ns
from api.data_processing import data_processing_ns

app = Flask(__name__)
api = Api(app, version='1.0', title='Right Sizing API',
          description='A simple Right Sizing API',
          doc='/swagger')  # Swagger UI endpoint

# Register the namespaces
api.add_namespace(health_ns, path='/health')

# Load data from the CSV file to Database
api.add_namespace(data_processing_ns)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
