from typing import List
from datetime import datetime
from fastapi import HTTPException
import google_auth_oauthlib.flow
import google.oauth2.credentials
import googleapiclient.discovery

from app.core.config import CLIENT_SECRETS_FILE, SCOPES, REDIRECT_URI
import app.core.config 
from app.interfaces.platform_interface import PlatformInterface
from app.interfaces.auth_interface import AuthInterface
from app.domain.models.media import Media, MediaType
from app.domain.models.comment import Comment


class YouTubeClient(PlatformInterface, AuthInterface):
    def __init__(self):
        super().__init__()


    # Login via YouTube API, utilizando OAuth
    async def get_login_url(self) -> str:
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, scopes=SCOPES
        )
        flow.redirect_uri = REDIRECT_URI

        authorization_url, _ = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true"
        )

        return authorization_url
    
    
    # Gera as credenciais do usuário
    async def handle_callback(self, code: str) -> bool:
        try:
            flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, scopes=SCOPES
            )
            flow.redirect_uri = REDIRECT_URI
            flow.fetch_token(code=code)

            app.core.config.user_credentials = flow.credentials

            return True
        
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Erro no callback: {str(e)}"
            )
        

    # Inicializa o cliente da API do YouTube
    def build_youtube_client(self):
        if not app.core.config.user_credentials:
            raise HTTPException(
                status_code=401, 
                detail="Usuário não autenticado."
            )
        
        return googleapiclient.discovery.build(
            "youtube",
            "v3",
            credentials=app.core.config.user_credentials,
            cache_discovery=False
        )
    

    # Retorna o id da playlist de uploads do canal
    def get_uploads_playlist_id(self, youtube) -> str:
        # Obtém as informações do canal autenticado (pega a playlist de uploads)
        channels_response = youtube.channels().list(
            part="contentDetails",
            mine=True
        ).execute()

        items = channels_response.get("items")
        
        if not items:
            raise HTTPException(
                status_code=404,
                detail="Nenhum canal encontrado para o usuário."
            )

        uploads_playlist_id = items[0]["contentDetails"]["relatedPlaylists"]["uploads"]
        
        return uploads_playlist_id
        
        
    # Cria uma lista com todas as mídias do canal
    async def fetch_medias(self) -> List[Media]:
        youtube = self.build_youtube_client()
        playlist_id = self.get_uploads_playlist_id(youtube)

        playlist_items = youtube.playlistItems().list(
            playlistId=playlist_id,
            part="snippet",
            maxResults=50
        ).execute()

        medias = []

        for item in playlist_items.get("items", []):
            video_id = item["snippet"]["resourceId"]["videoId"]

            # Obtém detalhes de cada vídeo (título, thumbnails, estatísticas)
            video_response = youtube.videos().list(
                id=video_id,
                part="snippet,statistics"
            ).execute()

            if not video_response["items"]:
                continue

            video = video_response["items"][0]
            snippet = video["snippet"]
            stats = video.get("statistics", {})

            # Inferindo tipo de mídia pela descrição
            if "#shorts" in snippet.get("description", "").lower():
                media_type = MediaType.VERTICAL
            else:
                media_type = MediaType.REGULAR

            medias.append(Media(
                id=video_id,
                format=media_type,
                image=snippet["thumbnails"]["default"]["url"],
                title=snippet["title"],
                publish_date=datetime.strptime(snippet["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"),
                view_count=int(stats.get("viewCount", 0)),
                comment_count=int(stats.get("commentCount", 0)),
                like_count=int(stats.get("likeCount", 0))
            ))

        return medias
    

    # Cria uma lista com todos os comentários de uma mídia
    async def fetch_comments(self, media_id: str) -> List[Comment]:
        youtube = self.build_youtube_client()

        try:
            comments_response = youtube.commentThreads().list(
                part="snippet",
                videoId=media_id,
                textFormat="plainText",
                maxResults=200
            ).execute()

            comments = []

            for item in comments_response.get("items", []):
                comment_id = item["id"]
                comment_text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]

                comments.append(Comment(
                    id=comment_id,
                    media_id=media_id,
                    text=comment_text
                ))

            return comments

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao buscar comentários: {str(e)}")


    # Deleta comentários da lista
    async def delete_comments(self, comment_ids: List[str]) -> bool:
        youtube = self.build_youtube_client()

        try:
            for comment_id in comment_ids:
                youtube.comments().setModerationStatus(
                    id=comment_id,
                    moderationStatus="rejected"
                ).execute()
            return True

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao deletar comentários: {str(e)}")
        