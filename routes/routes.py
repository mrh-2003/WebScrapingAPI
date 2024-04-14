from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from models.user import User
from models.user_register import UserRegister
from scraping.offshore_leaks_scraping import scrape_offshore_leaks
from scraping.ofac_scraping import scrape_ofac
from api.the_world_bank_api import search_the_world_bank_by_name

from auth.authentication import (
    get_active_user,
    register,
    login_user
)

router = APIRouter()

@router.post("/register")
def register_user(user: UserRegister):
    register(user)
    return {"message": "User successfully registered"}

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return {"access_token": login_user(form_data), "token_type": "bearer"}

@router.get("/search_offshore_leaks/{name}")
async def search_offshore_leaks(name: str, user: User = Depends(get_active_user)):
    try:
        table = scrape_offshore_leaks(name)
        return {
            "hits": len(table),
            "data": table,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/search_the_world_bank/{name}")
async def search_the_world_bank(name: str,  user: User = Depends(get_active_user)):
    try:
        table = search_the_world_bank_by_name(name)
        return {
            "hits": len(table),
            "data": table,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search_ofac/{name}")
async def search_ofac(name: str):
    try:
        table = scrape_ofac(name) 
        return {
            "hits": len(table),
            "data": table
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
