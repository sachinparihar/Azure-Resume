import azure.functions as func  # type: ignore
import logging
from azure.data.tables import TableServiceClient  # Updated import path
from azure.data.tables import TableEntity  # Updated import path

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Connection string for Azure Cosmos DB Table API
    connection_string = "DefaultEndpointsProtocol=https;AccountName=yourAccountName;AccountKey=yourAccountKey;TableEndpoint=https://yourAccountName.table.cosmos.azure.com:443/;"

    # Create TableServiceClient
    table_service = TableServiceClient.from_connection_string(conn_str=connection_string)

    # Name of the table
    table_name = "table1"

    # Fetch data from Cosmos DB Table API
    id = req.params.get('id')
    if id:
        try:
            # Assuming 'id' is the RowKey for the entities in your table
            table_client = table_service.get_table_client(table_name)
            entities = table_client.query_entities(f"RowKey eq '{id}'")
            for entity in entities:
                return func.HttpResponse(str(entity))
            return func.HttpResponse("Item not found", status_code=404)
        except Exception as e:
            logging.error(f"Error querying table: {e}")
            return func.HttpResponse("Error processing your request", status_code=500)
    else:
        # Return a response indicating that 'id' was not provided
        return func.HttpResponse("Please provide an id parameter", status_code=400)