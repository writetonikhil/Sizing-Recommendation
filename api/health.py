from flask_restx import Namespace, Resource

health_ns = Namespace('health_ns', description='Health check operations')

@health_ns.route('/')
class HealthCheck(Resource):
    def get(self):
        """
        Health check endpoint
        """
        return {'status': 'healthy'}, 200