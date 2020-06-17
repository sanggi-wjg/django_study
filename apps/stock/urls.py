from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from apps.stock.views import StockItemList, StockItemDetail, FinanceInfo, CreatePivotProc

urlpatterns = [
    path('item/', StockItemList.as_view()),
    path('item/<str:code>', StockItemDetail.as_view()),

    path('item/<str:code>/pivot', CreatePivotProc.as_view()),
    path('item/<str:code>/finance-info', FinanceInfo.as_view()),
]
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
