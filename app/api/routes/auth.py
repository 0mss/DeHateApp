from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from app.services.auth_service import AuthService
from app.api.dependencies import get_auth_service


# Cria um roteador para agrupar as rotas relacionadas à autenticação
# Prefixo /auth será aplicado a todas as rotas deste arquivo
router = APIRouter(prefix="/auth", tags=["Auth"])


# Rota GET para iniciar o processo de login com o Google (OAuth 2.0)
@router.get("/login")
async def login(auth_service: AuthService = Depends(get_auth_service)):
    login_url = await auth_service.get_login_url()
    return RedirectResponse(url=login_url)


# Rota GET que atua como callback do OAuth
@router.get("/callback")
async def auth_callback(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service)
):
    # Extrai o código de autorização (OAuth) dos parâmetros da URL
    code = request.query_params.get("code")

    if not code:
        raise HTTPException(
            status_code=400,
            detail="Código de autorização não fornecido."
        )
    # Processa o código de autorização com o serviço de autenticação
    success = await auth_service.handle_callback(code)

    # Redireciona o usuário conforme o sucesso ou falha do login
    if success:
        return RedirectResponse("myapp://auth/success")
    else:
        return RedirectResponse("myapp://auth/failure")
