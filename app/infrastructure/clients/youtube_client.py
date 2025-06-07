import os
import json
from typing import List
from datetime import datetime

from fastapi import HTTPException
import google_auth_oauthlib.flow
import google.oauth2.credentials
import googleapiclient.discovery

from app.core.config import SCOPES, REDIRECT_URI
import app.core.config  # necessário para acessar app.core.config.user_credentials

from app.interfaces.platform_interface import PlatformInterface
from app.interfaces.auth_interface import AuthInterface
from app.domain.models.media import Media, MediaType
from app.domain.models.comment import Comment


class YouTubeClient(PlatformInterface, AuthInterface):
    def __init__(self):
        super().__init__()

    async def get_login_url(self) -> str:
        client_secret_json_str = os.getenv("GOOGLE_CLIENT_SECRET_JSON")
        if not client_secret_json_str:
            raise HTTPException(status_code=500, detail="GOOGLE_CLIENT_SECRET_JSON não está definido")

        client_secret_dict = json.loads(client_secret_json_str)

        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            client_secret_dict, scopes=SCOPES
        )
        flow.redirect_uri = REDIRECT_URI

        authorization_url, _ = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true"
        )
        return authorization_url

    async def handle_callback(self, code: str) -> bool:
        try:
            client_secret_json_str = os.getenv("GOOGLE_CLIENT_SECRET_JSON")
            if not client_secret_json_str:
                raise HTTPException(status_code=500, detail="GOOGLE_CLIENT_SECRET_JSON não está definido")

            client_secret_dict = json.loads(client_secret_json_str)

            flow = google_auth_oauthlib.flow.Flow.from_client_config(
                client_secret_dict, scopes=SCOPES
            )
            flow.redirect_uri = REDIRECT_URI
            flow.fetch_token(code=code)

            # Guardando as credenciais globalmente (não recomendado para produção sem persistência segura)
            app.core.config.user_credentials = flow.credentials
            return True

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro no callback: {str(e)}")
