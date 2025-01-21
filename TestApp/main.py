from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from enum import Enum

app = FastAPI()

class WasteType(str, Enum):
    BIO = "bio"
    GLASS = "glass"
    PLASTIC = "plastic"

class Storage(BaseModel):
    id: int
    name: str
    capacity: Dict[WasteType, int]
    current_stock: Dict[WasteType, int]
    distances_to_organizations: Dict[str, int]
    connected_storages: Dict[int, int]  

class Organization(BaseModel):
    name: str
    waste_generated: Dict[WasteType, int]
    connected_storages: List[str]

organizations: Dict[str, Organization] = {}
storages: Dict[str, Storage] = {}


@app.post("/storages/", response_model=Storage)
def create_storage(storage: Storage):
    if storage.id in storages:
        raise HTTPException(status_code=400, detail="Storage already exists")
    storages[storage.name] = storage
    return storage

@app.post("/organizations/", response_model=Organization)
def create_organization(organization: Organization):
    if organization.name in organizations:
        raise HTTPException(status_code=400, detail="Organization already exists")
    organizations[organization.name] = organization
    return organization


@app.post("/transfer_waste/")
def transfer_waste_from_organization(organization_name: str, waste_to_transfer: Dict[WasteType, int]):
    if organization_name not in organizations:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    organization = organizations[organization_name]
    remaining_waste = waste_to_transfer.copy()
    logs = []

    for storage_name in sorted(organization.connected_storages, key=lambda s: storages[s].distances_to_organizations.get(organization_name, float("inf"))):
        storage = storages[storage_name]
        for waste_type, amount in list(remaining_waste.items()):
            if waste_type not in storage.capacity:
                continue
            free_space = storage.capacity[waste_type] - storage.current_stock.get(waste_type, 0)
            if free_space > 0:
                transferred = min(amount, free_space)
                storage.current_stock[waste_type] = storage.current_stock.get(waste_type, 0) + transferred
                remaining_waste[waste_type] -= transferred
                logs.append(f"{transferred} of {waste_type} transferred to {storage.name}")
                if remaining_waste[waste_type] == 0:
                    del remaining_waste[waste_type]
            if not remaining_waste:
                break
        if not remaining_waste:
            break

    if remaining_waste:
        logs.append(f"Remaining waste not transferred: {remaining_waste}")
    print(logs)
    return logs



@app.get("/storages/", response_model=List[Storage])
def get_storages():
    return list(storages.values())


@app.get("/organizations/", response_model=List[Organization])
def get_organizations():
    return list(organizations.values())