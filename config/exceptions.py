from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import (
    PermissionDenied,
    NotAuthenticated,
    ValidationError,
    AuthenticationFailed,
    Throttled,
)
from django.db import IntegrityError

def extract_error_message(detail):
    """
    Normalize DRF ErrorDetail / dict into clean string
    """
    if isinstance(detail, dict):
        if "detail" in detail:
            return str(detail["detail"])
        return "Authentication failed"

    return str(detail)



def custom_exception_handler(exc, context):
    """
    Production-grade global exception handler
    """

    # First let DRF handle it
    response = exception_handler(exc, context)

    # -------------------------------
    # 🔐 Auth / Permission Errors
    # -------------------------------
    if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        # raw_message = extract_error_message(exc.detail)
        raw = extract_error_message(exc.detail).lower()
        
        if "expired" in raw:
            message = "Token expired"
            error = "TOKEN_EXPIRED"
        elif "not found" in raw or "invalid" in raw:
            message = "Invalid token"
            error = "INVALID_TOKEN"
        else:
            message = "Authentication failed"
            error = "AUTH_FAILED"

        return Response(
            {
                "success" : False,
                "message" : "Invalid credentials",
                # "error" : raw_message,
                "error"   : error,
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if isinstance(exc, PermissionDenied):
        message = "You do not have permission to perform this action."
        raw_message = str(exc.detail) if exc.detail else message
        return Response(
            {
                "success" : False,
                "message" : message,
                "error"   : {"message": raw_message},
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    # -------------------------------
    # 🧪 Validation Errors
    # -------------------------------
    if isinstance(exc, ValidationError):
        return Response(
            {
                "success": False,
                "message": "Validation failed",
                "errors": response.data if response else exc.detail,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # -------------------------------
    # 🗄️ Database Integrity Errors
    # -------------------------------
    if isinstance(exc, IntegrityError):
        return Response(
            {
                "success": False,
                "message": "Database integrity error",
                "error": {
                    "message": "IntegrityError",
                    "details": str(exc),
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # -------------------------------
    # ⏱️ Throttling
    # -------------------------------
    if isinstance(exc, Throttled):
        return Response(
            {
                "success": False,
                "message": "Too many requests",
                "error": {
                    "message": str(exc.detail),
                    "wait": exc.wait,
                },
            },
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        )

    # -------------------------------
    # ❌ Unknown / Server Errors
    # -------------------------------
    if response is None:
        return Response(
            {
                "success": False,
                "message": "Internal server error",
                "error": {
                    "message": str(exc),
                },
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # -------------------------------
    # ✅ Default DRF handled errors
    # -------------------------------
    return Response(
        {
            "success": False,
            "message": "Request failed",
            "errors": response.data,
        },
        status=response.status_code,
    )
