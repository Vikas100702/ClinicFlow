from lib.lib_import import (
    APIRouter, Depends, HTTPException, Session, status, get_db,
    verify_password, create_access_token, get_current_user
)
from schema.auth_schema import UserLoginSchema, TokenResponseSchema
from models.user_role_model import UserModel

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Login API
@router.post("/login", response_model=TokenResponseSchema)
def login(login_data: UserLoginSchema, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == login_data.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
        )

    access_token = create_access_token(
        data={"sub": str(user.user_id), "role": user.role}
    )

    return TokenResponseSchema(access_token=access_token)

# Protected Route Example
@router.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {
        "message": f"Hello, {current_user['sub']}! Your role is {current_user['role']}."
    }
