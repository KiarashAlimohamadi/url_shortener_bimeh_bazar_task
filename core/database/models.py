#========================== IMPORTS ==================================

from sqlalchemy import Column,Integer,String,Text,DateTime,ForeignKey,func
from sqlalchemy.orm import relationship
from database.database import Base

#=====================================================================

#=================== DATABASE MODELS =================================
class UrlsModel(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String(2048), nullable=False)
    short_code = Column(String(16), nullable=False, unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    visit_count = Column(Integer, default=0, nullable=False)

    stats = relationship("StatsModel", back_populates="url")

    def __repr__(self):
        return (f"url : {self.id}")




class StatsModel(Base):
    __tablename__ = "stats"

    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(Integer, ForeignKey("urls.id"), nullable=False)
    ip = Column(String(45), nullable=False)
    visit_time = Column(DateTime, server_default=func.now())

    url = relationship("UrlsModel", back_populates="stats")

    def __repr__(self):
        return (f"stats for url : {self.url_id}, user_ip {self.ip}, visit time : {self.visit_time}")


#=====================================================================

