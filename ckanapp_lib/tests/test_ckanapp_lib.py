from urllib.parse import urljoin
from ckanapp_lib import get_app_params, CKAN_HOST_ENV, JSON_URL_ENV, BINARY_URL_ENV

from mock import patch
import mock, os, io, requests
from requests_mock import Mocker
from sure import expect
import sure

localhost = 'http://localhost'
ckan_host = localhost
json_url = '{}:6000/12345/json'.format(localhost)
binary_url = '{}:6000/12345/binary'.format(localhost)

JSON_ONLY = {
    CKAN_HOST_ENV: ckan_host,
    JSON_URL_ENV: json_url,
}
JSON_AND_BIN = {
    **JSON_ONLY,
    BINARY_URL_ENV: binary_url,
}

@patch.dict(os.environ, JSON_ONLY)
def test_response_keys_json_only():
    with Mocker() as m:
        m.get(json_url, json={})
        params = get_app_params()

    params.should.have.key('ckan_host')
    params.should.have.key('json_input')

@patch.dict(os.environ, JSON_AND_BIN)
def test_response_keys_json_and_binary():
    with Mocker() as m:
        m.get(json_url, json={})
        m.get(binary_url)
        params = get_app_params()

    params.should.have.key('ckan_host')
    params.should.have.key('json_input')
    params.should.have.key('binary_input')

@patch.dict(os.environ, JSON_ONLY)
def test_json_response():
    json_params = {'name': 'Cuong'}    
    
    with Mocker() as m:
        m.get(json_url, json=json_params)
        params = get_app_params()

    params['json_input'].should.equal(json_params)

@patch.dict(os.environ, JSON_AND_BIN)
def test_binary_response():
    
    with Mocker() as m:
        m.get(json_url, json={})
        m.get(binary_url, content=b'binary input')

        params = get_app_params()

    params['binary_input'].should.equal(b'binary input')

