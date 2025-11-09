from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from database import get_db
from profile.schema import Profile
from users.schema import User
from users.views import get_current_user


router = APIRouter(prefix="/profile", tags=["profile"])


class ProfileResponse(BaseModel):
    username: str
    email: EmailStr
    first_name: str | None = None


class ProfileUpdate(BaseModel):
    username: str
    email: EmailStr
    first_name: str | None = None


def _get_or_create_profile(db: Session, user: User) -> Profile:
    profile = db.query(Profile).filter(Profile.user_id == user.id).first()
    if profile is None:
        default_username = user.name or user.email.split("@")[0]
        default_first_name = user.name
        profile = Profile(
            user_id=user.id,
            username=default_username,
            first_name=default_first_name,
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile


@router.get("/", response_model=ProfileResponse)
def get_profile(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    profile = _get_or_create_profile(db, current_user)
    return ProfileResponse(
        username=profile.username,
        email=current_user.email,
        first_name=profile.first_name or "",
    )


@router.put("/", response_model=ProfileResponse)
def update_profile(
    profile_update: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = _get_or_create_profile(db, current_user)

    if profile_update.email != current_user.email:
        existing = (
            db.query(User)
            .filter(User.email == profile_update.email, User.id != current_user.id)
            .first()
        )
        if existing is not None:
            raise HTTPException(status_code=400, detail="Email already in use")
        current_user.email = profile_update.email

    current_user.name = profile_update.username
    profile.username = profile_update.username
    profile.first_name = profile_update.first_name

    db.add(current_user)
    db.add(profile)
    db.commit()
    db.refresh(current_user)
    db.refresh(profile)

    return ProfileResponse(
        username=profile.username,
        email=current_user.email,
        first_name=profile.first_name or "",
    )

