from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database.connection import get_db
from ..database.models import User, AuthProviders
from ..database.repository import UserRepository
from .schema import SignupSchema, LoginSchema, TokenResponse
from .security import verify_hash, create_access_token

auth = APIRouter()


@auth.post("/login", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def login(
    data: LoginSchema,
    db: Session = Depends(get_db)
):
    repo = UserRepository(db=db)
    # query the mail
    user = repo.get_by_email(data.email)

    # if not found -> error/ signup /wrong email /user not registered
    if not user or not verify_hash(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    access_token = await create_access_token(subject=str(user.id))

    return {'access_token': access_token}


@auth.post('/signup')
async def signup(
    data: SignupSchema,
    db: Session = Depends(get_db)
):

    # check if the user registered already
    user = db.query(User).filter(User.email == data.email).one_or_none()

    if user:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="User already exits"
        )

    if data.confirm_password != data.password:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Password doesn't match"
        )

    new = User(data.model_dump_json())

    db.add(new)
    db.commit()
    db.refresh()

    #  check that if confirm pass is as the password

    return {
        'email': new.email,
        'first_name': new.first_name
    }


@auth.post('/update')
async def update(db: Session = Depends(get_db)):
    email = "charantm@gmail.com"
    password = 'charantm'
    first_name = 'charan tm'
    primary_provider = AuthProviders.LocalAuthentication
    last_login_provider = AuthProviders.LocalAuthentication

    new = User(
        email=email,
        password=password,
        first_name=first_name,
        primary_provider=primary_provider,
        last_login_provider=last_login_provider
    )

    db.add(new)

    db.commit()
    return "user added successful"
