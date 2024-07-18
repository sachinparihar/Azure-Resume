import logging
import os
import azure.functions as func
from azure.data.tables import TableServiceClient
import json

# Correctly retrieve the connection string from environment variables
connection_string = os.environ['AZURE_CONNECTION_STRING']

# Now that 'connection_string' is defined, create the TableServiceClient instance
table_service = TableServiceClient.from_connection_string(conn_str=connection_string)

counter = 0  # Initialize counter variable

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    table_name = "Resumes"

    if req.method == "GET":
        # Get the id parameter from the request query string
        id = req.params.get('id')
        logging.info(f"Received id: {id}")

        # Check if the id parameter is provided
        if not id:
            return func.HttpResponse("Please provide an id parameter", status_code=400)

        try:
            # Query the CosmosDB table for the resume data
            table_client = table_service.get_table_client(table_name)
            # Assuming 'id' is unique and can serve as a RowKey
            entities = table_client.query_entities(f"RowKey eq '{id}'")
            for entity in entities:
                resume_data = {
                     'id': entity.get('RowKey'),
                    'name': entity.get('PartitionKey'),  # Adjusted from 'Name' to 'PartitionKey'
                    'kills': entity.get('Skills'),
                    'email': entity.get('Email'),
                    'experience': entity.get('Experience'),
                    # Ensure all necessary fields are included here
                }
                # Convert resume_data to JSON and return it
                return func.HttpResponse(json.dumps(resume_data), mimetype="application/json")
            # If no entities are found, return a not found response
            return func.HttpResponse("Resume not found", status_code=404)
        except Exception as e:
            logging.error(f"Error retrieving entity: {e}")
            return func.HttpResponse("Error retrieving resume data", status_code=500)

    elif req.method == "POST":
        global counter  # Declare counter as a global variable
        try:
            # Existing POST handling code
            req_body = req.get_json()
            if not req_body:
                return func.HttpResponse("Please provide a JSON payload", status_code=400)

            name = req_body.get('name')
            skills = req_body.get('skills')
            email = req_body.get('email')
            experience = req_body.get('experience')

            entity = {
                'PartitionKey': name,
                'RowKey': str(counter),
                'Name': name,
                'Skills': json.dumps(skills),
                'Email': email,
                'Experience': experience
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