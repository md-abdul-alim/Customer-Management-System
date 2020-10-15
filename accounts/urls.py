from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),

    path('', views.index, name='index'),
    path('profile/', views.profilePage, name='profile'),

    path('profile-settings/', views.profileSettings, name='profile-settings'),
    path('products/', views.products, name='products'),
    path('customer/<str:pk>/', views.customer, name='customer'),

    path('create_order/<str:pk>/', views.createOrder, name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),

    # password reset
    # https://docs.djangoproject.com/en/3.1/topics/auth/default/#django.contrib.auth.views.PasswordResetView
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
         name='password_reset'),
    # https://docs.djangoproject.com/en/3.1/topics/auth/default/#django.contrib.auth.views.PasswordResetDoneView
    path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'),
         name='password_reset_done'),
    # https://docs.djangoproject.com/en/3.1/topics/auth/default/#django.contrib.auth.views.PasswordResetConfirmView
    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'), name='password_reset_confirm'),
    # https://docs.djangoproject.com/en/3.1/topics/auth/default/#django.contrib.auth.views.PasswordResetConfirmView
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_complete'),
]
