import os
import socket
import subprocess
from lxml import etree
import suds.store
import suds.client
import pytest
import socket


import manage as flask_manage


@pytest.fixture(scope="session")
def app():
    app = flask_manage.app
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def flask_port():
    ## Ask OS for a free port.
    #
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        addr = s.getsockname()
        port = addr[1]
        return port

def _wait_for_tcp_port(host, port, timeout=2):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #presumably 
    sock.settimeout(timeout)
    try:
       sock.connect((host,port))
    except:
       return False
    else:
       sock.close()
       return True

@pytest.fixture(scope="session")
def flask_live_server(flask_port):
    env = os.environ.copy()
    env["FLASK_APP"] = "manage"
    server = subprocess.Popen(['flask', 'run', '--port', str(flask_port)], env=env)
    try:
        _wait_for_tcp_port('127.0.0.1', flask_port)
        yield server, f'http://127.0.0.1:{flask_port}'
    finally:
        server.terminate()



def test_hello(app, client):
    app.config.update({
        "HELLO": 'World',
    })
    response = client.get('/hello')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert response.json == {'hello': 'World'} 


def test_hello_http_rpc(client):
    response = client.get('/http_rpc/hello?times=5&name=Dave')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert response.json == ['Hello, Dave',] * 5


def test_hello_soap11(client):
    # Let's GET the WSDL
    response = client.get('/soap_11/?wsdl')
    assert response.status_code == 200
    assert response.content_type == 'text/xml; charset=utf-8'
    root = etree.XML(response.text.encode())
    assert root.nsmap['tns'] == 'spyne.examples.flask'


def test_hello_soap12(client):
    # Let's GET the WSDL
    response = client.get('/soap_12/?wsdl')
    assert response.status_code == 200
    assert response.content_type == 'text/xml; charset=utf-8'
    root = etree.XML(response.text.encode())
    assert root.nsmap['tns'] == 'spyne.examples.flask'



def test_hello_soap11_suds(flask_live_server):
    _p, base_url = flask_live_server
    service_url = f'{base_url}/soap_11/?wsdl'
    api = suds.client.Client(service_url)
    result = api.service.hello('Joe', 5)
    assert result.string == ['Hello, Joe',] * 5


@pytest.mark.skip(reason='SOAP 1.2 still does not work properly')
def test_hello_soap12_suds(flask_live_server):
    _p, base_url = flask_live_server
    service_url = f'{base_url}/soap_12/?wsdl'
    api = suds.client.Client(service_url)
    result = api.service.hello('Joe', 5)
    assert result.string == ['Hello, Joe',] * 5

    
