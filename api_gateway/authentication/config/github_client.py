from fastapi import HTTPException, status
from api_gateway.authentication.config import Oauth2


class GithubOAuthClient:

    async def fetch_github_userinfo(self, token: str) -> dict:
        try:
            user = await Oauth2.oauth.github.get('user', token=token)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Failed to fetch GitHub user info"
            )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Github user not found"
            )
        return user.json()
