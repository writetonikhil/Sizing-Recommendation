from flask_restx import fields
from api.data_processing import data_processing_ns

load_data_model = data_processing_ns.model('LoadDataModel', {
    'status' : fields.String(required=True, description='Status of the load data operation'),
    'data' : fields.List(fields.String, required=True, description='List of data loaded'),
    'error' : fields.String(description='Error message if any error occurs')
})
