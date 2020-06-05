from django.urls import path

from .views import SignUpView, LoginView, LogoutView, HomeView

urlpatterns = [
    path('', HomeView.as_view()),
    path('signup', SignUpView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
]
