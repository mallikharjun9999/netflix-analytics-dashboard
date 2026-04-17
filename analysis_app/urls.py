from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('search/', views.search, name='search'),
    path('detail/<str:show_id>/', views.detail, name='detail'),
    path('api/recommendations/', views.api_recommendations, name='api_recommendations'),
    path('api/chart-data/', views.api_chart_data, name='api_chart_data'),
    path('api/search/', views.api_search, name='api_search'),
]
