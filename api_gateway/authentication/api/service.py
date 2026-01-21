from datetime import datetime, timezone
from fastapi import HTTPException, status, BackgroundTasks

from api_gateway.authentication.api.security import create_access_token, create_hash, verify_hash
from api_gateway.authentication.database.models import AuthProviders, User
from api_gateway.authentication.database.repository import UserRepository
from api_gateway.authentication.api.schema import SignupSchema, LoginSchema


class AuthService:

    """
    Service layer for Authentication
    Handles all the business logic
    """

    def __init__(self, db):
        self.repo = UserRepository(db)

    def signup(self, data: SignupSchema, background_tasks: BackgroundTasks) -> str:
        self._ensure_email_not_taken(data.email)
        user = self._create_user(
            data,
            primary_provider=AuthProviders.LocalAuthentication,
            last_login_provider=AuthProviders.LocalAuthentication,
            last_login_at=datetime.now(timezone.utc)
        )

        background_tasks.add_task(

        )
        return self._issue_token(user)

    def login(self, data: LoginSchema) -> str:

        user = self.repo.get_by_email(data.email)
        self._ensure_user_availability_and_verify_password(
            user=user, data=data)
        self.repo.update_last_login(
            provider=AuthProviders.LocalAuthentication,
            user=user
        )
        return self._issue_token(user)
    

    # Internal helpers

    def _ensure_email_not_taken(self, email: str) -> None:
        if self.repo.exists_by_email(email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists",
            )

    def _create_user(
            self,
            data: SignupSchema,
            primary_provider: AuthProviders,
            last_login_at: datetime,
            last_login_provider: AuthProviders
    ) -> User:

        payload = data.model_dump(exclude={"password", "confirm_password"})
        payload.update(
            {
                "hashed_password": create_hash(data.password),
                "primary_provider": primary_provider,
                "last_login_at": last_login_at,
                "last_login_provider": last_login_provider
            }
        )
        return self.repo.create(**payload)

    def _issue_token(self, user: User) -> str:
        return create_access_token(subject=str(user.id))

    def _ensure_user_availability_and_verify_password(self, user: User, data: LoginSchema) -> None:
        if not user or not verify_hash(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Credentials"
            )
