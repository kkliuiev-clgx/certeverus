import json

from sqlalchemy import create_engine
from django.conf import settings

CONTENT_JSON = "application/json"

def make_request(client, route, data):
    response = client.post(route, data, content_type=CONTENT_JSON)
    returned_data = json.loads(response.content)
    
    message = returned_data.get('message', '')
    errors = returned_data.get('errors', {})
    redirect = returned_data.get('redirect', '')
    status_code = response.status_code

    return message, errors, redirect, status_code


def are_these_fields_flagged_for(*args, **kwargs):
    errors = kwargs.get('errors', '')
    fields = kwargs.get('fields',[])
    error_msg = kwargs.get('error_msg','')
    checks = list(map(lambda field: error_msg == errors.get(field,'') ,fields))
    return True if False in checks else False


def get_engine():
    """
    Get sqlalchemy engine
    """
    db_name = settings.DATABASES.get("default").get("NAME")
    user = settings.DATABASES.get("default").get("USER")
    password = settings.DATABASES.get("default").get("PASSWORD")
    host = settings.DATABASES.get("default").get("HOST")
    port = settings.DATABASES.get("default").get("PORT")

    # TODO - do we need utf8 ?
    # return create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db_name}", client_encoding="utf8")
    return create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db_name}")
