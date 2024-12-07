from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from customers import views

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/ads/'), name='logout'),
    path('signup/', views.sign_up, name='signup'),
    path('activation/', views.activation, name='activation')
]