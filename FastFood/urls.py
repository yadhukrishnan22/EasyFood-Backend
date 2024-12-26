"""
URL configuration for FastFood project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from api import views
from rest_framework.authtoken.views import ObtainAuthToken
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('api/signup/', views.SignUpView.as_view() ),
    path('api/token/', views.GetTokenView.as_view()),
    path('api/foodcat/add/', views.FoodCategoryCreateView.as_view()),
    path('api/foodcat/<int:pk>/', views.FoodCategoryRetrieveUpdateDestroyView.as_view()),
    path('api/food/add/', views.FoodCreateListView.as_view()),
    path('api/food/<int:pk>/', views.FoodRetrieveUpdateDestroyView.as_view())
    

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
