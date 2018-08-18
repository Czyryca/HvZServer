from django.urls import path

from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='longgame.html'), name='longgame'),
    path('', views.index, name='index'),
]
