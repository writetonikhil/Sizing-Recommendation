from flask import json, jsonify, request
from flask_restx import Namespace, Resource, reqparse
import pandas as pd
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest
from database.db import Base, ResourceUsage, get_engine
from sqlalchemy.orm import sessionmaker


data_processing_ns = Namespace('data_processing_ns', description='Data processing operations')

file_upload_parser = reqparse.RequestParser()
file_upload_parser.add_argument('file', 
                                location='files', 
                                type=FileStorage, 
                                required=True, 
                                help='csv file to upload'
                                )

@data_processing_ns.route('/api/v1/load_data')
class LoadData(Resource):
    @data_processing_ns.expect(file_upload_parser)
    @data_processing_ns.response(200, 'Success')
    @data_processing_ns.response(400, 'Invalid input')
    @data_processing_ns.response(500, 'Internal server error')
    def post(self):
        """
        Load data from the csv file
        """
        args = file_upload_parser.parse_args()
        file = args['file']
        print(f"File name: {file.filename}")
        
        try:
            df = pd.read_csv(file, encoding='utf-8')
            # csv_data = file.read().decode('utf-8')
            # Validate required columns
            expected_columns = {'index', 'cpu', 'ram', 'disk', 'network'}
            if not expected_columns.issubset(df.columns):
                return {"error": f"CSV must include headers: {expected_columns}"}, 400
            # Return CSV data
            # return  df.to_dict(orient='records'), 200  # Convert DataFrame to list of dicts
            # Save to database
            engine = get_engine()
            Base.metadata.create_all(engine)  # Create tables if they don't exist
            Session = sessionmaker(bind=engine)
            session = Session()

            for row in df.to_dict(orient='records'):
                resource_usage = ResourceUsage(
                    index_val=row['index'],
                    cpu=row['cpu'],
                    ram=row['ram'],
                    disk=row['disk'],
                    network=row['network'])
                session.add(resource_usage)

            session.commit()
            session.close()
            return {'message': 'Data loaded successfully'}, 200

        except BadRequest as e:
            return {'error': 'Bad request', 'details': str(e)}, 400
        except pd.errors.EmptyDataError:
            return {'error': 'Empty CSV file'}, 400
        except pd.errors.ParserError:
            return {'error': 'Invalid CSV file'}, 400
        except UnicodeDecodeError:
            return {'error': 'File encoding error'}, 400
        except FileNotFoundError:
            return {'error': 'File not found'}, 404
        except KeyError as e:
            return {'error': f'Missing required column: {str(e)}'}, 400
        except Exception as e:
            return {'error': 'An unexpected error occurred', 'details': str(e)}, 500
        finally:
            file.close()


@data_processing_ns.route('/api/v1/get_data')
class GetData(Resource):
    @data_processing_ns.response(200, 'Success')
    @data_processing_ns.response(400, 'Invalid input')
    @data_processing_ns.response(500, 'Internal server error')
    def get(self):
        """
        Get data from the database
        """
        try:
            engine = get_engine()
            Session = sessionmaker(bind=engine)
            session = Session()

            # Query all data
            data = session.query(ResourceUsage).all()
            session.close()

            # Convert to list of dictionaries
            data_list = [
                {
                    'index': row.index_val,
                    'cpu': row.cpu,
                    'ram': row.ram,
                    'disk': row.disk,
                    'network': row.network
                } for row in data
            ]

            return data_list, 200

        except Exception as e:
            return {'error': 'An unexpected error occurred', 'details': str(e)}, 500