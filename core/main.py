#======================= IMPORTS ===============================
from fastapi import FastAPI
from url_shortener.routes import router as url_routers


#===============================================================


#==================== SETUP ====================================

app = FastAPI()
app.include_router(url_routers)


