import os, requests

CKAN_HOST_ENV = 'CKAN_HOST'
JSON_URL_ENV = 'JSON_INPUT_URL'
FILE_URL_ENV = 'BINARY_INPUT_URL'

def get_app_params():
    ckan_host = os.getenv(CKAN_HOST_ENV)
    json_url = os.getenv(JSON_URL_ENV)
    file_url = os.getenv(FILE_URL_ENV, None)

    # TODO: raise exception & handle?
    ret = {
        'ckan_host': ckan_host,
        'json': requests.get(json_url).json(),
    }

    if file_url:
        ret['file'] = requests.get(file_url).content

    return ret