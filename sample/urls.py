"""sample URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apps.in_queue.views import InQueue
from apps.sign.views import HomeView, SignUpView, LoginView, LogoutView
from apps.stock.views import StockItemList, StockItemDetail, CreatePivotProc, FinanceInfo

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomeView.as_view()),
    path('signup', SignUpView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),

    path('stocks/item/', StockItemList.as_view()),
    path('stocks/item/<str:code>', StockItemDetail.as_view()),
    path('stocks/item/<str:code>/pivot', CreatePivotProc.as_view()),
    path('stocks/item/<str:code>/finance-info', FinanceInfo.as_view()),

    path('data/in-queue/', InQueue.as_view()),
]
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls))
    ]