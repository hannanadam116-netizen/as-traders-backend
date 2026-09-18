from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Company
from .serializers import CompanySerializer


class CompanyView(APIView):
    """
    GET    : Get Company Details
    POST   : Create Company (Only Once)
    PUT    : Update Company
    """

    def get(self, request):

        company = Company.objects.first()

        if company is None:
            return Response(
                {
                    "message": "Company not created."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CompanySerializer(company)

        return Response(serializer.data)

    def post(self, request):

        # Allow only one company
        if Company.objects.exists():
            return Response(
                {
                    "error": "Company already exists."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CompanySerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def put(self, request):

        company = Company.objects.first()

        if company is None:
            return Response(
                {
                    "error": "Company not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CompanySerializer(
            company,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(serializer.data)


class CompanyDetailView(APIView):
    """
    GET : Company Details
    """

    def get(self, request):

        company = Company.objects.first()

        if company is None:
            return Response(
                {
                    "message": "Company not created."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CompanySerializer(company)

        return Response(serializer.data)