from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum
from .models import Transaction
from .serializers import TransactionSerializer
from django.http import JsonResponse

class TransactionCreate(APIView):
    def post(self, request, format=None):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "ok"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransactionDetail(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    lookup_field = 'id'

class TransactionType(APIView):
    def get(self, request, type, format=None):
        transactions = Transaction.objects.filter(type=type).values()
        return Response(list(transactions), status=status.HTTP_200_OK)

class TransactionSum(generics.RetrieveAPIView):
    serializer_class = TransactionSerializer
    lookup_field = 'id'
    
    def calculate_sum(self, transaction_id):
        transaction_sum = {}
        if transaction_id not in transaction_sum:
            # Get the immediate child transactions and their sums
            child_transactions = Transaction.objects.filter(parent_id=transaction_id)
            child_sum = sum(self.calculate_sum(child.id) for child in child_transactions)
            
            # Calculate the total sum for this transaction
            transaction = Transaction.objects.get(id=transaction_id)
            transaction_sum[transaction_id] = transaction.amount + child_sum
        
        return transaction_sum[transaction_id]

    def get(self, request, *args, **kwargs):
        transaction_id = kwargs['id']
        total_amount = self.calculate_sum(transaction_id)
        return JsonResponse({'sum': total_amount})