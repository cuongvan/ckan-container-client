from urllib.parse import urljoin
from ckanapp_lib import get_app_params, CKAN_HOST_ENV, JSON_URL_ENV, FILE_URL_ENV

from mock import patch
import mock, os, io, requests
from requests_mock import Mocker
from sure import expect
import sure

localhost = 'http://localhost'
ckan_host = localhost
json_url = '{}:6000/12345/json'.format(localhost)
file_url = '{}:6000/12345/binary'.format(localhost)

JSON_ONLY = {
    CKAN_HOST_ENV: ckan_host,
    JSON_URL_ENV: json_url,
}
JSON_AND_FILE = {
    **JSON_ONLY,
    FILE_URL_ENV: file_url,
}

@patch.dict(os.environ, JSON_ONLY)
def test_response_keys_json_only():
    with Mocker() as m:
        m.get(json_url, json={})
        params = get_app_params()

    params.should.have.key('ckan_host')
    params.should.have.key('json')

@patch.dict(os.environ, JSON_AND_FILE)
def test_response_keys_json_and_binary():
    with Mocker() as m:
        m.get(json_url, json={})
        m.get(file_url)
        params = get_app_params()

    params.should.have.key('ckan_host')
    params.should.have.key('json')
    params.should.have.key('file')

@patch.dict(os.environ, JSON_ONLY)
def test_json_response():
    json_params = {'name': 'Cuong'}    
    
    with Mocker() as m:
        m.get(json_url, json=json_params)
        params = get_app_params()

    params.should.have.key('json').being.equal(json_params)

@patch.dict(os.environ, JSON_AND_FILE)
def test_binary_response():
    file_content = b'binary input'

    with Mocker() as m:
        m.get(json_url, json={})
        m.get(file_url, content=file_content)

        params = get_app_params()

    params.should.have.key('file').being.equal(file_content)

