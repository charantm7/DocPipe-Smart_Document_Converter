import httpx
from fastapi import APIRouter, Request

from ..settings import settings

upload = APIRouter()


@upload.api_route("/upload/{path:path}", methods=["GET", "POST"])
async def proxy_upload(path: str, request: Request):
    body = await request.body()

    async with httpx.AsyncClient() as client:
        resp = await client.request(
            method=request.method,
            url=f"{settings.UPLOAD_SERVICE_URL}/upload/{path}",
            headers=dict(request.headers),
            content=body
        )

    return resp.json()
