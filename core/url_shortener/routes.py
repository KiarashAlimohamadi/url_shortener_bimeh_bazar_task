#====================== IMPORTS ==========================

from fastapi import APIRouter,Path,Depends,HTTPException,status
from fastapi import Request
from fastapi.responses import JSONResponse
from database.models import StatsModel,UrlsModel
from sqlalchemy.orm import Session
from database.database import get_db
import random
import string
from .schemas import URLCreateSchema,URLResponseSchema
from fastapi.responses import RedirectResponse
from sqlalchemy import update

#==========================================================

#================= ROUTER SETUP ===========================
router = APIRouter(tags=["url_shortener"],prefix="")
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




@router.get('/{short_code}')
async def redirect(short_code: str, request: Request, db: Session = Depends(get_db)):
    url = db.query(UrlsModel).filter(UrlsModel.short_code == short_code).first()
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Short URL not found")
    db.execute(
        update(UrlsModel)
        .where(UrlsModel.id == url.id)
        .values(visit_count=UrlsModel.visit_count + 1)
    )
    stat = StatsModel(url_id=url.id,ip=request.client.host)
    db.add(stat)
    db.commit()
    db.refresh(stat)
    return RedirectResponse(url=url.original_url,status_code=status.HTTP_302_FOUND)


@router.get("/stats/{short_code}")
async def show_stats(short_code:str,db : Session = Depends(get_db)):
    url = db.query(UrlsModel).filter(UrlsModel.short_code==short_code).first()
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Short URL not found")
    visit_count = url.visit_count
    return JSONResponse(content={
        "visit_count" : visit_count
    },status_code=status.HTTP_302_FOUND)







