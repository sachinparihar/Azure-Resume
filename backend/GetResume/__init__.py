import logging
import os
import azure.functions as func
from azure.data.tables import TableServiceClient
import json

connection_string = os.environ['AZURE_CONNECTION_STRING']

table_service = TableServiceClient.from_connection_string(conn_str=connection_string)

counter = 0  

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    table_name = "table1"

    if req.method == "GET":
        id = req.params.get('id')
        logging.info(f"Received id: {id}")

        if not id:
            return func.HttpResponse("Please provide an id parameter", status_code=400)

        try:
            table_client = table_service.get_table_client(table_name)
            entities = table_client.query_entities(f"RowKey eq '{id}'")
            for entity in entities:
                resume_data = {
                     'id': entity.get('RowKey'),
                    'name': entity.get('PartitionKey'),  
                    'basics': json.loads(entity.get('Basics')),
                    'work': json.loads(entity.get('Work')),
                    'education': json.loads(entity.get('Education')),
                    'awards': json.loads(entity.get('Awards')),
                    'kills': json.loads(entity.get('Skills')),
                    'interests': json.loads(entity.get('Interests')),
                }
                return func.HttpResponse(json.dumps(resume_data, cls=json.JSONEncoder), mimetype="application/json")
            return func.HttpResponse("Resume not found", status_code=404)
        except Exception as e:
            logging.error(f"Error retrieving entity: {e}")
            return func.HttpResponse("Error retrieving resume data", status_code=500)

    elif req.method == "POST":
        global counter  
        try:
            req_body = req.get_json()
            if not req_body:
                return func.HttpResponse("Please provide a JSON payload", status_code=400)

            basics = req_body.get('basics')
            work = req_body.get('work')
            education = req_body.get('education')
            awards = req_body.get('awards')
            skills = req_body.get('skills')
            interests = req_body.get('interests')

            entity = {
                'PartitionKey': basics.get('name'),
                'RowKey': str(counter),
                'Basics': json.dumps(basics, cls=json.JSONEncoder),
                'Work': json.dumps(work, cls=json.JSONEncoder),
                'Education': json.dumps(education, cls=json.JSONEncoder),
                'Awards': json.dumps(awards, cls=json.JSONEncoder),
                'Skills': json.dumps(skills, cls=json.JSONEncoder),
                'Interests': json.dumps(interests, cls=json.JSONEncoder)
            }

            counter += 1

            table_client = table_service.get_table_client(table_name)
            table_client.create_entity(entity)

            return func.HttpResponse("Resume created successfully", status_code=201)
        except Exception as e:
            logging.error(f"Error creating entity: {e}")
            return func.HttpResponse("Error creating resume", status_code=500)

    else:
        return func.HttpResponse("Invalid request method", status_code=405)