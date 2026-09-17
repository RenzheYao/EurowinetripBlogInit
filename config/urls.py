"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from Eurowinetrip.sitemaps import PostSitemap  # Import your new class
from django.contrib.sitemaps.views import sitemap

# Define the sitemaps dictionary
sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),

    #path('api/login/', auth_views.obtain_auth_token), # Regular DRF Token
    path('api/', include('Eurowinetrip.urls')),

    # Djoser URLs
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    # JWT URLs (if you want to use them directly)
    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    path('ckeditor/', include('ckeditor_uploader.urls')), # Add this line
    
    # The Sitemap URL
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
] 

# Serve media files ONLY during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
