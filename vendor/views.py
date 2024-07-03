from django.shortcuts import render
from vendor.models import *
from vendor.serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from openpyxl import Workbook
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from rest_framework.permissions import AllowAny,IsAuthenticated



# create vendor
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_vendor(request):
    if request.method == 'POST':
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'OK',
                'message': 'vendor created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# vendors list
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vendor_list(request):
    if request.method == 'GET':
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response({
                'status': 'OK',
                'message': 'vendors listed successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
    
# detail,edit and delete vendor
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def vendor_detail(request, pk):
    try:
        vendor = Vendor.objects.get(pk=pk)
    except Vendor.DoesNotExist:
        return Response({
            'status': 'Not Found',
            'message': 'Vendor not found'
        }, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VendorSerializer(vendor)
        return Response({
            'status': 'OK',
            'message': 'Vendor retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'OK',
                'message': 'Vendor updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        vendor.delete()
        return Response({
            'status': 'OK',
            'message': 'Vendor deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)
    

# transaction create
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_transaction(request):
    if request.method == 'POST':
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save()

           
            vendor_name = transaction.vendor.name if transaction.vendor else None

          
            response_data = {
                'status': 'OK',
                'message': 'Transaction created successfully',
                'data': {
                    'id': transaction.id,
                    'vendor_name': vendor_name,
                    'description': transaction.description,
                    'amount': transaction.amount
                }
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# transaction list
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_list(request):
    if request.method == 'GET':
        transactions = Transaction.objects.all()
        data = []
        for transaction in transactions:
            transaction_data = {
                'id': transaction.id,
                'vendor_name': transaction.vendor.name if transaction.vendor else None,
                'description': transaction.description,
                'amount': transaction.amount
            }
            data.append(transaction_data)
        return Response({
            'status': 'OK',
            'message': 'List of transactions',
            'data': data
        })


# transaction details
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_detail(request, pk):
    try:
        transaction = Transaction.objects.get(pk=pk)
    except Transaction.DoesNotExist:
        return Response({
            'status': 'Not Found',
            'message': 'Transaction not found'
        }, status=status.HTTP_404_NOT_FOUND)

    
    vendor_name = transaction.vendor.name if transaction.vendor else None


    response_data = {
        'status': 'OK',
        'message': 'Transaction details',
        'data': {
            'id': transaction.id,
            'vendor_name': vendor_name,
            'description': transaction.description,
            'amount': transaction.amount
        }
    }
    return Response(response_data)

# transaction edit
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_transaction(request, pk):
    try:
        transaction = Transaction.objects.get(pk=pk)
    except Transaction.DoesNotExist:
        return Response({
            'status': 'Not Found',
            'message': 'Transaction not found'
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = TransactionSerializer(transaction, data=request.data)
    if serializer.is_valid():
        serializer.save()

        
        vendor_name = transaction.vendor.name if transaction.vendor else None

     
        response_data = {
            'status': 'OK',
            'message': 'Transaction updated successfully',
            'data': {
                'id': transaction.id,
                'vendor_name': vendor_name,
                'description': transaction.description,
                'amount': transaction.amount
            }
        }
        return Response(response_data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# transaction delete
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_transaction(request, pk):
    try:
        transaction = Transaction.objects.get(pk=pk)
    except Transaction.DoesNotExist:
        return Response({
            'status': 'Not Found',
            'message': 'Transaction not found'
        }, status=status.HTTP_404_NOT_FOUND)

    transaction.delete()
    return Response({
        'status': 'OK',
        'message': 'Transaction deleted successfully'
    }, status=status.HTTP_204_NO_CONTENT)


# add excel to transactions
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_excel(request):
    transactions = Transaction.objects.all()

   
    wb = Workbook()
    ws = wb.active
    ws.title = "Transactions"

    headers = ['Vendor', 'Description', 'Amount']
    ws.append(headers)

    
    for transaction in transactions:
        ws.append([transaction.vendor.name, transaction.description, transaction.amount])

   
    response = HttpResponse(content_type='application/vnd.openpyxl.sheet')
    response['Content-Disposition'] = 'attachment; filename=transactions.xlsx'
    wb.save(response)

    return response