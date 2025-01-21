import pytest
from fastapi.testclient import TestClient
from main import app, WasteType

BASE_URL = "http://127.0.0.1:8000" 
client = TestClient(app)

@pytest.fixture
def setup_data():
    client.post(f"{BASE_URL}/storages/", json={
        "id": 1,
        "name": "MHO1",
        "capacity": {"glass": 100, "plastic": 50},
        "current_stock": {"glass": 0, "plastic": 0},
        "distances_to_organizations": {"OO1": 10, "OO2": 50},
        "connected_storages": {}
    })
    client.post(f"{BASE_URL}/storages/", json={
        "id": 2,
        "name": "MHO2",
        "capacity": {"bio": 200},
        "current_stock": {"bio": 0},
        "distances_to_organizations": {"OO1": 30},
        "connected_storages": {}
    })
    client.post(f"{BASE_URL}/organizations/", json={
        "name": "OO1",
        "waste_generated": {"glass": 50, "plastic": 30},
        "connected_storages": ["MHO1", "MHO2"]
    })
    client.post(f"{BASE_URL}/organizations/", json={
        "name": "OO2",
        "waste_generated": {"bio": 100},
        "connected_storages": ["MHO2"]
    })



def test_create_storage():
    #Test: storage create
    response = client.post(f"{BASE_URL}/storages/", json={
        "id": 3,
        "name": "MHO3",
        "capacity": {"bio": 150},
        "current_stock": {"bio": 0},
        "distances_to_organizations": {"OO1": 20},
        "connected_storages": {1: 20}
    })
    assert response.status_code == 200
    assert response.json()["name"] == "MHO3"


def test_create_organization():
    #Test: org create
    response = client.post(f"{BASE_URL}/organizations/", json={
        "name": "OO3",
        "waste_generated": {"glass": 20},
        "connected_storages": ["MHO1"]
    })
    assert response.status_code == 200
    assert response.json()["name"] == "OO3"


def test_transfer_waste_success(setup_data):
    #Test: successful waste transfer
    response = client.post(f"{BASE_URL}/transfer_waste/", params={"organization_name": "OO1"}, json={
        "glass": 30,
        "plastic": 20
    })
    assert response.status_code == 200
    assert "30 of WasteType.GLASS transferred to MHO1" in response.json()
    assert "20 of WasteType.PLASTIC transferred to MHO1" in response.json()


def test_transfer_waste_partial(setup_data):
    #Test: partial waste transfer
    response = client.post(f"{BASE_URL}/transfer_waste/", params={"organization_name": "OO1"}, json={
        "glass": 150
    })
    print(response)
    assert response.status_code == 200
    assert "100 of WasteType.GLASS transferred to MHO1" in response.json()
    assert "Remaining waste not transferred: {<WasteType.GLASS: 'glass'>: 50}" in response.json()


def test_transfer_waste_no_storage(setup_data):
    #Test: error when there is no available storage
    response = client.post(f"{BASE_URL}/transfer_waste/", params={"organization_name": "OO2"}, json={
        "plastic": 10
    })
    assert response.status_code == 200
    assert "Remaining waste not transferred: {<WasteType.PLASTIC: 'plastic'>: 10}" in response.json()


def test_get_storages(setup_data):
    #Test: getting a list of storages
    response = client.get(f"{BASE_URL}/storages/")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_organizations(setup_data):
    #Test: getting a list of organizations
    response = client.get(f"{BASE_URL}/organizations/")
    assert response.status_code == 200
    assert len(response.json()) == 3