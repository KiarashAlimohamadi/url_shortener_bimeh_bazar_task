#====================== IMPORTS ==========================

from fastapi import APIRouter,Path,Depends,HTTPException
from fastapi.responses import JSONResponse
from database.models import StatsModel,UrlsModel
from sqlalchemy.orm import Session
from database.database import get_db

#==========================================================

#================= ROUTER SETUP ===========================
router = APIRouter(tags=["url_shortener"],prefix="/short")
#==========================================================


#================= ROUTES =================================

