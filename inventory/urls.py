from django.urls import path
from . import views

urlpatterns = [
    path('add-box/',views.AddBox.as_view(),name='add-box'),
]
