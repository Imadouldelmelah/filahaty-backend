from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/farmer", tags=["Farmer Verification"])

# Pydantic Models for requests and responses
class FarmerRegistrationRequest(BaseModel):
    firstName: str = Field(..., description="First name of the farmer")
    lastName: str = Field(..., description="Last name of the farmer")
    phoneNumber: str = Field(..., description="Phone number")
    farmerCardId: str = Field(..., description="Farmer card ID")
    nationalIdCard: str = Field(..., description="National ID card number")
    language: str = Field(default="fr", description="Preferred language")

class FarmerLoginRequest(BaseModel):
    phoneNumber: str
    nationalIdCard: str

class FarmerResponse(BaseModel):
    id: str
    firstName: str
    lastName: str
    phoneNumber: str
    farmerCardId: str
    nationalIdCard: str
    language: str
    isVerified: bool
    createdAt: str
    lastLoginAt: str

# Mock Database for demo purposes
MOCK_FARMER_DB = {}

@router.post("/register", response_model=dict)
async def register_farmer(request: FarmerRegistrationRequest):
    # Check for duplicates based on phone or national ID
    for f_id, f_data in MOCK_FARMER_DB.items():
        if f_data["phoneNumber"] == request.phoneNumber or f_data["nationalIdCard"] == request.nationalIdCard:
            raise HTTPException(status_code=400, detail="Farmer account already exists with this phone number or national ID.")
    
    farmer_id = f"FARMER_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    new_farmer = {
        "id": farmer_id,
        "firstName": request.firstName,
        "lastName": request.lastName,
        "phoneNumber": request.phoneNumber,
        "farmerCardId": request.farmerCardId,
        "nationalIdCard": request.nationalIdCard,
        "language": request.language,
        "isVerified": True,
        "createdAt": datetime.now().isoformat(),
        "lastLoginAt": datetime.now().isoformat()
    }
    
    MOCK_FARMER_DB[farmer_id] = new_farmer
    
    return {
        "status": "success",
        "message": "Farmer registered successfully",
        "data": new_farmer
    }

@router.post("/login", response_model=dict)
async def login_farmer(request: FarmerLoginRequest):
    for f_id, f_data in MOCK_FARMER_DB.items():
        if f_data["phoneNumber"] == request.phoneNumber and f_data["nationalIdCard"] == request.nationalIdCard:
            f_data["lastLoginAt"] = datetime.now().isoformat()
            MOCK_FARMER_DB[f_id] = f_data
            return {
                "status": "success",
                "message": "Login successful",
                "data": f_data
            }
            
    raise HTTPException(status_code=401, detail="Invalid phone number or national ID.")

@router.get("/profile/{farmer_id}", response_model=dict)
async def get_farmer_profile(farmer_id: str):
    farmer = MOCK_FARMER_DB.get(farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found.")
        
    return {
        "status": "success",
        "data": farmer
    }

@router.put("/update/{farmer_id}", response_model=dict)
async def update_farmer_profile(farmer_id: str, request: FarmerRegistrationRequest):
    if farmer_id not in MOCK_FARMER_DB:
        raise HTTPException(status_code=404, detail="Farmer not found.")
        
    updated_data = MOCK_FARMER_DB[farmer_id]
    updated_data.update(request.dict(exclude_unset=True))
    MOCK_FARMER_DB[farmer_id] = updated_data
    
    return {
        "status": "success",
        "message": "Profile updated successfully",
        "data": updated_data
    }

@router.post("/logout", response_model=dict)
async def logout_farmer():
    return {
        "status": "success",
        "message": "Logged out successfully"
    }
