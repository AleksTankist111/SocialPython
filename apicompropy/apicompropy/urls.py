"""apicompropy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django_registration.backends.one_step.views import RegistrationView
from exercise.forms import CustomUserForm
from django.conf import settings
from .views import IndexTemplateView

urlpatterns = [
    path('admin/', admin.site.urls),                        # Путь для админ-панельки
    path('accounts/register/',
         RegistrationView.as_view(form_class=CustomUserForm, success_url='/'),
         name='django_registration_register'),              # Путь для регистрации
    path('auth/', include('django.contrib.auth.urls')),     # Путь для логин-логаут сессиями

    path('api-auth/', include('rest_framework.urls')),      # Специальный путь для тестирования (логининга в drf браузере)

    re_path(r'^auth/', include('djoser.urls.authtoken')),   # Путь для api-token логин-логаут
    path('api/v1/', include('exercise.urls')),              # Путь с пользовательскими api


    re_path(r'^.*$', IndexTemplateView.as_view(), name='entry-point')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


