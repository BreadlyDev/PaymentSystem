from django.urls import path
from . import views as v

urlpatterns = [
    path('all', v.TransactionListAPIView.as_view()),
    path('create', v.TransactionCreateAPIView.as_view()),
    path('<uuid:id>', v.TransactionChangeAPIView.as_view()),
]
