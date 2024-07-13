import azure.functions as func  # type: ignore
import logging
from azure.data.tables import TableServiceClient  # Updated import path
from azure.data.tables import TableEntity  # Updated import path
import json
import os
from dotenv import load_dotenv  # Import load_dotenv from python-dotenv

# Load environment variables from .env file
load_dotenv()

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger", methods=["GET", "POST"])
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Connection string for Azure Cosmos DB Table API
    connection_string = os.getenv('AZURE_CONNECTION_STRING')

    # Create TableServiceClient
    table_service = TableServiceClient.from_connection_string(conn_str=connection_string)

    # Name of the table
    table_name = "Resumes"

    if req.method == "GET":
        # Fetch data logic remains the same as before
        id = req.params.get('id')
        if id:
            try:
                table_client = table_service.get_table_client(table_name)
                entities = table_client.query_entities(f"RowKey eq '{id}'")
                for entity in entities:
                    return func.HttpResponse(str(entity))
                return func.HttpResponse("Item not found", status_code=404)
            except Exception as e:
                logging.error(f"Error querying table: {e}")
                return func.HttpResponse("Error processing your request", status_code=500)
        else:
            return func.HttpResponse("Please provide an id parameter", status_code=400)
    elif req.method == "POST":
        try:
            # Extract data from request body
            data = req.get_json()
            # Create or update entity in table
            table_client = table_service.get_table_client(table_name)
            entity = TableEntity()
            for key, value in data.items():
                entity[key] = value
            table_client.upsert_entity(entity=entity)
            return func.HttpResponse("Entity created or updated successfully", status_code=201)
        except Exception as e:
            logging.error(f"Error inserting/updating entity: {e}")
            return func.HttpResponse("Error processing your request", status_code=500)