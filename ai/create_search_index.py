import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import ConnectionType
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from config import get_logger

# initialize logging object

logger = get_logger(__name__)

# create a project client using environment variables loaded from the .env file
project = AIProjectClient.from_connection_string(
    conn_str=os.environ["AIPROJECT_CONNECTION_STRING"], credential=DefaultAzureCredential()
)

# create a vector embeddings client that will be used to generate vector embeddings
embeddings = project.inference.get_embeddings_client()

# use the project client to get the default search connection
search_connection = project.connections.get_default(
    connection_type=ConnectionType.AZURE_AI_SEARCH, include_credentials=True
)

# Create a search index client using the search connection
# This client will be used to create and delete search indexes
index_client = SearchIndexClient(
    endpoint=search_connection.endpoint_url, credential=AzureKeyCredential(key=search_connection.key)
)