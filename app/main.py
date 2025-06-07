import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth as auth_router
from app.api.routes import media as media_router

app = FastAPI(
    title=".DeHate API",
    version="1.0.0",
    description="API do .DeHate, seu app de limpeza de redes sociais."
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(media_router.router)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # pega a PORT ou usa 8000 padrão
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
