from api.views import scan_item
from django.urls import path


urlpatterns = [
    path('item/<str:item_id>/scan', scan_item, name='scan_item')
]