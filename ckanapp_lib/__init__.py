import os, requests

CKAN_HOST_ENV = 'CKAN_HOST'
JSON_URL_ENV = 'JSON_INPUT_URL'
BINARY_URL_ENV = 'BINARY_INPUT_URL'

def get_app_params():
    ckan_host = os.getenv(CKAN_HOST_ENV)
    json_input_url = os.getenv(JSON_URL_ENV)
    binary_input_url = os.getenv(BINARY_URL_ENV, None)

    # TODO: raise exception & handle?
    ret = {
        'ckan_host': ckan_host,
        'json': requests.get(json_input_url).json(),
    }

    if binary_input_url:
        ret['file'] = requests.get(binary_input_url).content

    return ret