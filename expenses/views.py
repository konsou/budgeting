from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from expenses.models import Account, Category, Expense
from expenses.serializers import ExpenseSerializer


class ExpenseCreateView(APIView):
    def post(self, request, format=None):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
