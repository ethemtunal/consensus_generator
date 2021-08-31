from django.urls import path
from .views import *

urlpatterns = [
    path('images/', ImageAPIView.as_view()),
    path('images/<uuid:pk>/', ImageDetailAPIView.as_view()),
    path('images/calculate/<uuid:pk>', CalculateImageConsensus.as_view()),
    path('annotators/', AnnotatorAPIView.as_view()),
    path('annotators/<uuid:pk>/', AnnotatorDetailAPIView.as_view()),
    path('annotations/', AnnotationAPIView.as_view()),
    path('annotations/<uuid:pk>/', AnnotationDetailAPIView.as_view()),
    path('consensus/', ConsensusAPIView.as_view()),
    path('consensus/calculate/', CalculateConsensusAPIView.as_view()),
]