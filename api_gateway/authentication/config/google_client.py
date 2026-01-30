import httpx
from fastapi import HTTPException, status


class GoogleOAuthClient:
    USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
    VALID_ISSUERS = {"https://accounts.google.com", "accounts.google.com"}

    async def fetch_userinfo(self, access_token: str) -> dict:
        async with httpx.AsyncClient() as client:
            reponse = await client.get(
                self.USERINFO_URL,
                headers={
                    "Authorization": f"Bearer {access_token}"
                }
            )

        if reponse.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Failed to fetch Google user info"
            )

        return reponse.json()

    def validate_user(self, iss: str):
        if iss not in self.VALID_ISSUERS:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Google authentication failed.")
