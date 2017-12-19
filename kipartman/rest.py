# preliminaries
import swagger_client

base_url = 'http://localhost:8200/api'
client_id = ''
client_secret = ''

unauthenticated_client = None
client = None
api = None
model = None

def reload():
    global unauthenticated_client
    global client
    global api
    global model
    
    unauthenticated_client = swagger_client.ApiClient(base_url)
    client = swagger_client.ApiClient(base_url)
    api = swagger_client.DefaultApi(client)
    model = swagger_client

reload()