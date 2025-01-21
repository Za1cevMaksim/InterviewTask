import requests

BASE_URL = "http://127.0.0.1:8000"

def test_transfer_waste(organization_name, waste_to_transfer):
    response = requests.post(
        f"{BASE_URL}/transfer_waste/",
        params={"organization_name": organization_name}, 
        json=waste_to_transfer  
    )
    print(f"Test for organization {organization_name} with waste {waste_to_transfer}:")
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.json()}")

test_transfer_waste("OO1", {"glass": 50, "plastic": 10})
test_transfer_waste("OO2", {"bio": 50, "plastic": 60})
test_transfer_waste("OO1", {"bio": 200, "plastic": 10})