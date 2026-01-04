#====================== IMPORTS ==========================

from fastapi import APIRouter,Path,Depends,HTTPException
from fastapi.responses import JSONResponse
from database.models import StatsModel,UrlsModel
from sqlalchemy.orm import Session
from database.database import get_db
import random
import string
from .schemas import URLCreateSchema,URLResponseSchema

#==========================================================

#================= ROUTER SETUP ===========================
router = APIRouter(tags=["url_shortener"],prefix="/short")
#==========================================================

#=============== FUNCTIONS ================================
def generate_short_code(length :int = 8) -> str:
    choices = string.ascii_letters + string.digits
    return ''.join(random.choices(choices, k=length))

#==========================================================



#================= ROUTES =================================

@router.post("/shorten",response_model=URLResponseSchema)
async def shorten_url(request:URLCreateSchema,db : Session = Depends(get_db)):
    short_code = generate_short_code()
    new_url = UrlsModel(original_url = request.url,short_code=short_code)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url





