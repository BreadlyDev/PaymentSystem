from django.urls import path
from . import views as v

urlpatterns = [
    path('all', v.AppListAPIView.as_view()),
    path('create', v.AppCreateAPIView.as_view()),
    path('all/analytics', v.AppAnalyticsAPIView.as_view()),
    path('<int:pk>', v.AppAPIView.as_view()),
]
