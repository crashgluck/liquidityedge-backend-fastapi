from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import *
from app.models.user import User, UserStatus, UserRole
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token
from app.core.config import get_settings
from app.db.session import get_db
from app.services.email_ses import send_2fa_email
import random, datetime

router = APIRouter()
settings = get_settings()


def validate_domain(email: str):
    domain = email.split("@")[-1]
    return domain in settings.DOMAIN_WHITELIST


@router.post("/register")
def register_user(payload: RegisterRequest, db: Session = Depends(get_db)):
    # Email único
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(400, "Email already registered")

    # Validación dominio corporativo
    if payload.role == "fund_manager" and not validate_domain(payload.email):
        status = UserStatus.pending
    else:
        status = UserStatus.active

    # Crear usuario con TODOS los atributos nuevos
    user = User(
        # básicos
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=UserRole(payload.role),
        status=status,

        # nuevos (si existen en el payload)
        name=payload.name,
        company=payload.company,
        title=payload.title,
        mobile=payload.mobile,
        business_type=payload.business_type,
        portal_used=payload.portal_used,
        total_investment=payload.total_investment or 0,

        # términos y condiciones
        terms_accepted=payload.terms_accepted,
        terms_accepted_date=datetime.datetime.utcnow() if payload.terms_accepted else None,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "Registered", "status": user.status.value}


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(400, "Invalid credentials")

    if user.status != UserStatus.active:
        raise HTTPException(403, "User not approved")

    code = str(random.randint(100000, 999999))
    user.twofa_code = code
    user.twofa_expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    db.commit()

    send_2fa_email(user.email, code)

    return {"access_token": "pending-2fa", "token_type": "bearer"}


@router.post("/2fa/verify", response_model=TokenResponse)
def verify_2fa(payload: Verify2FARequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(404, "User not found")

    if user.twofa_code != payload.code:
        raise HTTPException(400, "Invalid code")

    if datetime.datetime.utcnow() > user.twofa_expires:
        raise HTTPException(400, "Code expired")

    token = create_access_token({"sub": str(user.id), "role": user.role.value})

    user.twofa_code = None
    db.commit()

    return TokenResponse(access_token=token)
