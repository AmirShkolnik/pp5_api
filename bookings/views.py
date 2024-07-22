from django.db import IntegrityError
from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer
import logging

logger = logging.getLogger(__name__)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        logger.info(f"Attempting to create booking for user "
                    f"{request.user.username}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user=self.request.user)
                headers = self.get_success_headers(serializer.data)
                logger.info(f"Booking created successfully for user "
                            f"{request.user.username}")
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED,
                                headers=headers)
            except IntegrityError:
                logger.warning("Booking creation failed: Duplicate booking "
                               "attempt")
                error_message = ("A booking for this course, date, and time "
                                 "already exists. Please choose a different "
                                 "date or time.")
                return Response({"non_field_errors": [error_message]},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.error(f"Booking creation failed: {serializer.errors}")
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        if serializer.is_valid():
            confirm = request.data.get('confirm', False)
            if not confirm:
                return Response({
                    "message": "Are you sure you want"
                    "to change the date, time, or course?",
                    "requires_confirmation": True
                }, status=status.HTTP_200_OK)
            try:
                self.perform_update(serializer)
                logger.info(f"Booking updated successfully for user "
                            f"{request.user.username}")
                return Response(serializer.data)
            except IntegrityError:
                logger.warning("Booking update failed: Duplicate booking "
                               "attempt")
                error_message = ("A booking for this course, date, and time "
                                 "already exists. Please choose a different "
                                 "date or time.")
                return Response({"non_field_errors": [error_message]},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.error(f"Booking update failed: {serializer.errors}")
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        logger.info(f"Booking deleted successfully for user "
                    f"{request.user.username}")
        return Response(status=status.HTTP_204_NO_CONTENT)
