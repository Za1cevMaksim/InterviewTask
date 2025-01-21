import requests

BASE_URL = "http://127.0.0.1:8000" 

def create_storage(id, name, max_capacity, distances_to_organizations, connected_storages):
    response = requests.post(f"{BASE_URL}/storages/", json={
        "id": id,
        "name":name,
        "capacity": max_capacity,
        "current_stock": {waste_type: 0 for waste_type in max_capacity.keys()},
        "distances_to_organizations": distances_to_organizations,
        "connected_storages": connected_storages
    })
    if response.status_code != 200:
        print(f"Failed to create storage '{id}': {response.json()}")

def create_organization(name, waste_generated, connected_storages):
    response = requests.post(f"{BASE_URL}/organizations/", json={
        "name": name,
        "waste_generated": waste_generated,
        "connected_storages": connected_storages
    })
    if response.status_code != 200:
        print(f"Failed to create organization '{name}': {response.json()}")


def generate_test_data():
    create_storage(
        id=1,
        name="MHO1",
        max_capacity={"glass": 300, "plastic": 100},
        distances_to_organizations={"OO1": 100},
        connected_storages={8: 500}
    )
    
    create_storage(
        id=2,
        name="MHO2",
        max_capacity={"bio": 150, "plastic": 50},
        distances_to_organizations={"OO1": 50},
        connected_storages={5: 50}
    )

    create_storage(
        id=3,
        name="MHO3",
        max_capacity={"plastic": 10, "bio": 250},
        distances_to_organizations={"OO1": 600, "OO2": 50},
        connected_storages={6: 600, 7: 50}
    )

    create_storage(
        id=5,
        name="MHO5",
        max_capacity={"glass": 220, "bio": 25},
        distances_to_organizations={"OO1": 100},
        connected_storages={2: 50}
    )
    create_storage(
        id=6,
        name="MHO6",
        max_capacity={"glass": 100, "bio": 150},
        distances_to_organizations={},
        connected_storages={}
    )
    create_storage(
        id=7,
        name="MHO7",
        max_capacity={"plastic": 100, "bio": 250},
        distances_to_organizations={},
        connected_storages={3: 50}
    )
    create_storage(
        id=8,
        name="MHO8",
        max_capacity={"glass":35,"plastic": 25, "bio": 52},
        distances_to_organizations={},
        connected_storages={9: 10}
    )

    create_storage(
        id=9,
        name="MHO9",
        max_capacity={"plastic": 250, "bio": 20},
        distances_to_organizations={},
        connected_storages={9: 10}
    )

    create_organization(
        name="OO1",
        waste_generated={"bio": 50, "glass": 50, "plastic": 10},
        connected_storages=["MHO1", "MHO2", "MHO3", "MHO5", "MHO6", "MHO7", "MHO8", "MHO9"]
    )

    create_organization(
        name="OO2",
        waste_generated={"bio": 50, "glass": 20, "plastic": 60},
        connected_storages=["MHO1", "MHO2", "MHO3", "MHO5", "MHO6", "MHO7", "MHO8", "MHO9"]
    )
    

if __name__ == "__main__":
    generate_test_data()