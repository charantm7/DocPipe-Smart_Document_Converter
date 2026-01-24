from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.orm import Session

from api_gateway.authentication.api.service import AuthService, EmailService, get_current_user
from api_gateway.authentication.database.connection import get_db
from api_gateway.authentication.database.models import User, AuthProviders
from api_gateway.authentication.database.repository import UserRepository
from api_gateway.authentication.api.schema import SignupSchema, LoginSchema, TokenResponse, PasswordResetRequestSchema, PasswordResetSchema

auth = APIRouter()


@auth.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED
)
async def login(
    data: LoginSchema,
    db: Session = Depends(get_db)
):
    return {'access_token': AuthService(db).login(data)}


@auth.post(
    '/signup',
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED
)
async def signup(
    data: SignupSchema,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    return {'access_token': AuthService(db).signup(
        data=data,
        background_tasks=background_tasks
    )}


@auth.post(
    "/verify-email"
)
async def verify_email(
    token: str,
    db: Session = Depends(get_db)
):
    return EmailService(db).validate_email_verification_link(token)


@auth.post(
    "/resend-email-verification"
)
async def resend_email_verification(
    background_task: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return EmailService(db).resend_verification_link(
        user=current_user,
        backround_task=background_task
    )


@auth.post("/reset-password-request")
async def reset_password_request(
    data: PasswordResetRequestSchema,
    db: Session = Depends(get_db)
):
    return AuthService(db).create_and_send_password_reset_link(data.email)


@auth.post('/reset-password')
async def reset_password(
    token: str,
    data: PasswordResetSchema,
    db: Session = Depends(get_db)
):
    return AuthService(db).reset_password_from_token(token, data)
