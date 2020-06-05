from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View


class HomeView(View):
    def get(self, request):
        return render(request, 'comm/home.html', {
            'view_title': 'Home',
            'is_auth'   : request.user.is_authenticated,
        })


class SignUpView(View):
    def get(self, request):
        return render(request, 'sign/signup.html', {
            'view_title': 'Signup',
            'user_form' : UserCreationForm()
        })

    def post(self, request):
        user_form = UserCreationForm(data = request.POST)

        if user_form.is_valid():
            user = user_form.save()
            print('USER_FORM:', user_form)
            print('USER:', user)
            authenticate(username = user.username, passowrd = user.password)

            return HttpResponseRedirect('/')

        else:
            return render(request, 'sign/signup.html', {
                'view_title': 'Signup',
                'user_form' : UserCreationForm(),
                'error'     : user_form.errors,
                'error_msg' : user_form.error_messages
            })


class LoginView(View):
    def get(self, request):
        return render(request, 'sign/login.html', {
            'view_title': 'Login',
            'login_form': AuthenticationForm()
        })

    def post(self, request):
        login_form = AuthenticationForm(request, request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect(settings.LOGIN_URL)

        else:
            return render(request, 'sign/login.html', {
                'view_title': 'Login',
                'login_form': AuthenticationForm(),
                'error_msg' : '다시!'
            })


class LogoutView(View):

    def get(self, request):
        logout(request)

        return HttpResponseRedirect(settings.LOGIN_URL)
