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

from apps.etf.views import EtfList
from apps.func.views import FinancialMetrics, IndexSites, IndexFinancialDataImage
from apps.trend.views import InvestorTrend, InvestorTrendData
# from apps.in_queue.views import InQueue, InQueueOne
from apps.portfolio.views import PortfolioList, CreatePortfolio, PortfolioDetail, StockSearchAutocomplete, PortfolioStockPurchase, PortfolioStockSell
from apps.sector.views import SectorDetail, SectorList, SectorFinancialDataComparedPriceImage
from apps.sign.views import HomeView, SignUpView, LoginView, LogoutView
from apps.stock.views import StockDetail, CreatePivotProc, ScrapFinancialInfo, ScrapDemandInfo, SearchStockNSectorList, StockList, StockPriceChartData
from apps.zzz.views import ZZZController

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomeView.as_view()),
    path('signup', SignUpView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),

    # 기업
    path('stocks/company', StockList.as_view()),
    path('stocks/company/list', SearchStockNSectorList.as_view()),
    path('stocks/company/<str:stock_code>', StockDetail.as_view()),
    path('stocks/company/<str:stock_code>/chart/<str:from_date>/<str:to_date>', StockPriceChartData.as_view()),
    path('stocks/company/<str:stock_code>/pivot', CreatePivotProc.as_view()),
    # path('stocks/<str:code>/finance-info', FinanceInfo.as_view()),
    path('stocks/company/<str:stock_code>/scrap-financial', ScrapFinancialInfo.as_view()),
    path('stocks/company/<str:stock_code>/scrap-demand', ScrapDemandInfo.as_view()),

    # 업종
    path('stocks/sector', SectorList.as_view()),
    path('stocks/sector/<str:sector_id>', SectorDetail.as_view()),
    path('stocks/sector/<str:sector_id>/<str:term>/financial/image', SectorFinancialDataComparedPriceImage.as_view()),

    # ETF
    path('stocks/etf', EtfList.as_view()),
    path('stocks/etf/<str:company_id>', EtfList.as_view()),

    # Investor trend
    path('stocks/trend/<str:market>', InvestorTrend.as_view()),
    path('stocks/trend/<str:market>/<str:from_date>/<str:to_date>', InvestorTrendData.as_view()),

    # Portfolio
    path('portfolios', PortfolioList.as_view(), name = '포트폴리오 리스트'),
    path('portfolios/create', CreatePortfolio.as_view(), name = '포트폴리오 생성'),
    path('portfolios/stock/search', StockSearchAutocomplete.as_view(), name = '포트폴리오 매수시 종목 검색'),

    path('portfolios/<str:portfolio_id>', PortfolioDetail.as_view(), name = '포트폴리오 상세'),
    path('portfolios/<str:portfolio_id>/stock/purchase', PortfolioStockPurchase.as_view(), name = '포트폴리오 상세 종목 매수'),
    path('portfolios/<str:portfolio_id>/stock/sell', PortfolioStockSell.as_view(), name = '포트폴리오 상세 종목 매도'),

    # 부가기능
    path('func/financial-metrics', FinancialMetrics.as_view(), name = '재무지표'),
    path('func/indexs', IndexSites.as_view(), name = '인덱스 지표 리스트'),
    path('func/indexs/<str:fd_type>/<str:term>/financial/image', IndexFinancialDataImage.as_view(), name = '인덱스 지표 plot 이미지'),

    path('zzz', ZZZController.as_view(), name = 'zzz'),

    # path('data/in-queue/', InQueue.as_view()),
    # path('data/in-queue/<str:productCd>', InQueueOne.as_view()),
]
from apps.trend.views import InvestorTrend, InvestorTrendData

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
