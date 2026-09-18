from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    LoginSerializer,
    ChangePasswordSerializer,
)

from .services import AccountService


# =====================================================
# LOGIN
# =====================================================

class LoginView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.validated_data["user"]

        return Response(

            AccountService.login(user),

            status=status.HTTP_200_OK,

        )


# =====================================================
# PROFILE
# =====================================================

class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response(

            AccountService.profile(
                request.user
            )

        )


# =====================================================
# CHANGE PASSWORD
# =====================================================

class ChangePasswordView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ChangePasswordSerializer(

            data=request.data

        )

        serializer.is_valid(

            raise_exception=True

        )

        result = AccountService.change_password(

            request.user,

            serializer.validated_data[
                "old_password"
            ],

            serializer.validated_data[
                "new_password"
            ],

        )

        return Response(result)


# =====================================================
# LOGOUT
# =====================================================

class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        refresh = request.data.get("refresh")

        if not refresh:

            return Response(

                {

                    "error":
                        "Refresh token required."

                },

                status=status.HTTP_400_BAD_REQUEST,

            )

        result = AccountService.logout(
            refresh
        )

        return Response(result)