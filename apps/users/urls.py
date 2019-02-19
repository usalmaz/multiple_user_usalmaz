from django.urls import path
from .views import UserRegistrationView, CabinetView, PostCreateView, PostUpdateView, PostDetailView, PostDeleteView
from . import views

app_name = 'users'

urlpatterns = [
    path('accounts/register/', UserRegistrationView.as_view(), name='register'),
    path('accounts/cabinet/', CabinetView.as_view(), name='cabinet'),
    path('accounts/cabinet/blog/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('accounts/cabinet/new/', PostCreateView.as_view(), name='post-create'),
    path('accounts/cabinet/blog/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('accounts/cabinet/blog/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('', views.home, name='home'),
    path('accounts/cabinet/blog/', views.blog, name='blog'),
    path('accounts/cabinet/countries/', views.countries, name='countries'),
    path('accounts/cabinet/cities/<int:pk>/', views.cities, name='cities'),
    path('accounts/cabinet/address/<int:pk>/', views.address, name='address'),


]
