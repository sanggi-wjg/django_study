from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import StockItemList, StockItemDetail, CreatePivotProc

urlpatterns = [
    path('item/', StockItemList.as_view()),
    path('item/<str:code>', StockItemDetail.as_view()),

    # path('item/<str:code>/pivot', CreatePivot.as_view()),
    path('item/<str:code>/pivot', CreatePivotProc.as_view()),
]
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
