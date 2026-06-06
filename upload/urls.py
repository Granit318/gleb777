from django.urls import path

from upload.views import items_list, upload_json

urlpatterns = [
    path('', upload_json, name='upload_json'),
    path('items/', items_list, name='items_list'),
]
