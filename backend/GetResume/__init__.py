import logging
import os
import uuid
import azure.functions as func
from azure.data.tables import TableServiceClient
import json

# Correctly retrieve the connection string from environment variables
connection_string = os.environ['AZURE_CONNECTION_STRING']

# Now that 'connection_string' is defined, create the TableServiceClient instance
table_service = TableServiceClient.from_connection_string(conn_str=connection_string)

counter = 0  # Initialize the counter variable

def main(req: func.HttpRequest) -> func.HttpResponse:
    global counter  # Declare counter as a global variable

    logging.info('Python HTTP trigger function processed a request.')

    table_name = "Resumes"

    try:
        # Get the request body as JSON
        req_body = req.get_json()
        if not req_body:
            return func.HttpResponse("Please provide a JSON payload", status_code=400)

        # Extract the required fields from the request body
        name = req_body.get('name')
        skills = req_body.get('skills')
        email = req_body.get('email')
        experience = req_body.get('experience')

        # Create a new entity
        entity = {
            'PartitionKey': name,
            'RowKey': str(counter),  # Use the counter as the RowKey
            'Name': name,
            'Skills': json.dumps(skills),  # Convert skills list to JSON string
            'Email': email,
            'Experience': experience
        }

        # Increment the counter
        counter += 1

        # Insert the entity into the table
        table_client = table_service.get_table_client(table_name)
        table_client.create_entity(entity)

        # Return a success response
        return func.HttpResponse("Resume created successfully", status_code=201)
    except Exception as e:
        logging.error(f"Error creating entity: {e}")
        return func.HttpResponse("Error creating resume", status_code=500)