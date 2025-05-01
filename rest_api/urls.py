from django.contrib import admin
from django.urls import path, include
from .views import (UserRegistration1View, UserRegistration2View, UserRegistration3View, LogoutView, ForgotPasswordView,
                    ResetPasswordView, ProfileView, ChangePasswordAuthview, CVdownloadView, CVdeleteView, CompanyView, CompanyInfoView,
                    JobsView, JobDetailView, ChatsView, MessagesView, NotificationView,NotificationUpdateView, CVView, CVDeleteAPIView, CVUpdateView)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="ISH BOR",
        default_version='v1',
        description="Demo ISH BOR API",
        terms_of_service='DEMO.COM',
        contact=openapi.Contact(email='<EMAIL>'),
        license=openapi.License(name='demo service')
    ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
)


urlpatterns = [
    path('auth/verify-email/', UserRegistration1View.as_view()),
    path('auth/verify-email/confirm/', UserRegistration2View.as_view()),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/verify-email/createuser/', UserRegistration3View.as_view()),
    path('auth/password/forgot/', ForgotPasswordView.as_view()),
    path('auth/password/reset/', ResetPasswordView.as_view()),
    path('auth/password/change/', ChangePasswordAuthview.as_view()),
    path('profile/', ProfileView.as_view()),
    path("profile/upload-cv/", CVdownloadView.as_view()),
    path('profile/delete-cv/', CVdeleteView.as_view()),
    path('company/', CompanyView.as_view()),
    path('company/<int:company_id>/', CompanyInfoView.as_view(), name='company-info'),
    path('jobs/', JobsView.as_view()),
    path('jobs/<int:job_id>/', JobDetailView.as_view()),
    path('chats/', ChatsView.as_view()),
    path('chats/<int:chat_id>/messages/', MessagesView.as_view()),
    path('notification/<int:job_id>/', NotificationView.as_view()),
    path('notification/update/<int:notification_id>/', NotificationUpdateView.as_view()),
    path('cv/', CVView.as_view()),
    path('cv/upload/', CVUpdateView.as_view()),
    path('cv/<int:pk>/delete/', CVDeleteAPIView.as_view()),
    path('docs-redoc/', schema_view.with_ui("redoc", cache_timeout=0), name='redoc'),
    path('docs-swagger/', schema_view.with_ui("swagger", cache_timeout=0), name='swagger'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
