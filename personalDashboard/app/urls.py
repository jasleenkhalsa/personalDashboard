from django.urls import path
from . import views

urlpatterns = [
    path('', views.auth_view, name='auth'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('item/create/', views.item_create, name='item_create'),
    path('item/update/<int:pk>/', views.item_update, name='item_update'),
    path('item/delete/<int:pk>/', views.item_delete, name='item_delete'),
]
