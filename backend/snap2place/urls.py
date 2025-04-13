from django.urls import path
from .views import LandmarkPredictView

urlpatterns = [
    path('predict/', LandmarkPredictView.as_view(), name='predict'),
]
