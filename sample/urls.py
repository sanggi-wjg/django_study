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

from apps.func.views import FinancialMetrics, IndexSites, IndexFinancialDataImage
# from apps.in_queue.views import InQueue, InQueueOne
from apps.sector.views import SectorDetail, SectorList, SectorFinancialDataComparedPriceImage
from apps.sign.views import HomeView, SignUpView, LoginView, LogoutView
from apps.stock.views import StockDetail, CreatePivotProc, ScrapFinancialInfo, ScrapDemandInfo, StockSearchCompanyList, StockList

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomeView.as_view()),
    path('signup', SignUpView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),

    # 기업
    path('stocks', StockList.as_view()),
    path('stocks/list', StockSearchCompanyList.as_view()),
    path('stocks/<str:stock_code>', StockDetail.as_view()),
    path('stocks/<str:stock_code>/pivot', CreatePivotProc.as_view()),
    # path('stocks/<str:code>/finance-info', FinanceInfo.as_view()),
    path('stocks/<str:stock_code>/scrap-financial', ScrapFinancialInfo.as_view()),
    path('stocks/<str:stock_code>/scrap-demand', ScrapDemandInfo.as_view()),

    # 업종
    path('sector', SectorList.as_view()),
    path('sector/<str:sector_id>', SectorDetail.as_view()),
    path('sector/<str:sector_id>/<str:term>/financial/image', SectorFinancialDataComparedPriceImage.as_view()),

    # 부가기능
    path('func/financial-metrics', FinancialMetrics.as_view()),
    path('func/indexs', IndexSites.as_view()),
    path('func/indexs/<str:fd_type>/<str:term>/financial/image', IndexFinancialDataImage.as_view()),

    # path('data/in-queue/', InQueue.as_view()),
    # path('data/in-queue/<str:productCd>', InQueueOne.as_view()),
]
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

# urlpatterns += [
#     path('swagger<str:format>', schema_view.without_ui(cache_timeout = 0), name = 'schema-json'),
#     path('swagger/', schema_view.with_ui('swagger', cache_timeout = 0), name = 'schema-swagger-ui'),
#     path('docs/', schema_view.with_ui('redoc', cache_timeout = 0), name = 'schema-redoc'),
# ]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls))
    ]
