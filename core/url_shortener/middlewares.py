from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import update
from datetime import datetime
from database.database import SessionLocal
from database.models import UrlsModel, StatsModel




class ShortURLLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        response = await call_next(request)

        path = request.url.path.lstrip("/")

        if (request.method == "GET" and path and path != "shorten"and not path.startswith("stats")):

            db: Session = SessionLocal()

            try:
                url = (db.query(UrlsModel).filter(UrlsModel.short_code == path).first())

                if url:
                    db.execute(update(UrlsModel).where(UrlsModel.id == url.id).values(visit_count=UrlsModel.visit_count + 1))

                    stat = StatsModel(url_id=url.id,ip=request.client.host,visit_time=datetime.utcnow())
                    db.add(stat)
                    db.commit()
            finally:
                db.close()
        return response
