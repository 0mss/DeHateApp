from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from app.infrastructure.clients.youtube_client import YouTubeClient

router = APIRouter(prefix="/auth", tags=["Auth"])

youtube_client = YouTubeClient()


# Rota para iniciar o login (faz redirect para o Google OAuth)
@router.get("/login")
async def login():
    login_url = await youtube_client.get_login_url()
    return RedirectResponse(url=login_url)


# Callback do Google (backend processa o token e responde ao front)
@router.get("/callback")
async def auth_callback(request: Request):
    code = request.query_params.get("code")

    if not code:
        raise HTTPException(
            status_code=400,
            detail="Código de autorização não fornecido."
        )

    success = await youtube_client.handle_callback(code)

    if success:
        return RedirectResponse("myapp://auth/success")
    else:
        return RedirectResponse("myapp://auth/failure")
