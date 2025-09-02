from lib.lib_import import (
    APIRouter, Depends, HTTPException, Session, status, get_db,
    create_access_token, decode_access_token, hash_password,
    verify_password, timedelta
)
from models.user_role_model import UserModel

router = APIRouter(prefix = "/forgot_password", tags = ["Forgot Password"])

@router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == email).first()

    if not user:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email does not exist"
        )
    
    # craete token valid for 30 minutes
    reset_token = create_access_token(
         data = {
              "sub": user.email,
              "action": "reset_password"
         },
         expires_delta = timedelta(minutes = 30)
    )

    return {
         "message": "Password reset token generated", 
         "reset_token": reset_token
    }


# reset password
@router.post("/reset-password")
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(token.strip('"'))
        if payload.get("action") != "reset_password":
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND, 
                detail="Invalid token type"
            )

        email = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Invalid token"
            )
        user = db.query(UserModel).filter(UserModel.email == email).first()
        if not user:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND, 
                detail="User not found"
            )

        # update password
        user.password = hash_password(new_password)
        db.commit()
        return {"message": "Password reset successful"}

    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail="Invalid or expired token"
        )