#======================= IMPORTS ===============================
from fastapi import FastAPI
from url_shortener.routes import router as url_routers
from url_shortener.middlewares import ShortURLLoggingMiddleware

#===============================================================


#==================== SETUP ====================================

app = FastAPI()
app.include_router(url_routers)
app.add_middleware(ShortURLLoggingMiddleware)


