from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer


class AccountService:

    # ==========================================
    # LOGIN
    # ==========================================

    @staticmethod
    def login(user):

        refresh = RefreshToken.for_user(user)

        return {

            "access": str(refresh.access_token),

            "refresh": str(refresh),

            "user": UserSerializer(user).data,

        }

    # ==========================================
    # PROFILE
    # ==========================================

    @staticmethod
    def profile(user):

        return UserSerializer(user).data

    # ==========================================
    # CHANGE PASSWORD
    # ==========================================

    @staticmethod
    def change_password(

        user,

        old_password,

        new_password,

    ):

        if not user.check_password(old_password):

            return {

                "success": False,

                "message":
                    "Old password is incorrect.",

            }

        user.set_password(new_password)

        user.save()

        return {

            "success": True,

            "message":
                "Password changed successfully.",

        }

    # ==========================================
    # LOGOUT
    # ==========================================

    @staticmethod
    def logout(refresh_token):

        token = RefreshToken(refresh_token)

        token.blacklist()

        return {

            "success": True,

            "message": "Logged out successfully.",

        }