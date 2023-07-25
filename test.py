import pytest
import docker
client = docker.from_env()
import subprocess
import requests
from time import sleep
from retry import retry

# Arrange
@pytest.fixture
def fixture_env():
    container = client.containers.run("ealen/echo-server", ports={'80/tcp':8080}, detach=True)
    address = "http://localhost:8080"
    try_connection(address)
    yield address
    container.kill()

@retry(tries=15, delay=0.1)
def try_connection(address):
    requests.get(address)
#    return r.status_code

def send_request(address):
    return requests.get(f'{address}/param', params={"query": "demo"})

def test_fruit_salad(fixture_env):
    # Act

    r = send_request(fixture_env)

    r.json()

    # Assert
    assert r.json()
