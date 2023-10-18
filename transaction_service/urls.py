from django.urls import path
from .views import TransactionDetail, TransactionType, TransactionSum, TransactionCreate

urlpatterns = [
    path('transactionservice/transaction/', TransactionCreate.as_view(), name='transaction-create'),
    path('transactionservice/transaction/<int:id>', TransactionDetail.as_view(), name='transaction-detail'),
    path('transactionservice/types/<str:type>', TransactionType.as_view(), name='transaction-type'),
    path('transactionservice/sum/<int:id>', TransactionSum.as_view(), name='transaction-sum'),
]
