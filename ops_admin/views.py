from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from ops_admin.models import Order, Retailer, Supplier, Concession, Memo, ManualOrder
from ops_admin.serializers import UserSerializer, OrderSerializer, RetailerSerializer, SupplierSerializer, \
                                    ConcessionSerializer, MemoSerializer, ManualOrderSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


"""

API ROOT

"""

@api_view(['GET'])
def api_root(request, format=None):

    """Endpoints below, authentication required."""

    return Response({
        'users': reverse('user-list', request=request, format=format),
        'orders': reverse('order-list', request=request, format=format),
        'retailers': reverse('retailer-list', request=request, format=format),
        'suppliers': reverse('supplier-list', request=request, format=format),
        'concessions': reverse('concession-list', request=request, format=format),
        'memos': reverse('memo-list', request=request, format=format),
        'manual orders': reverse('manual-list', request=request, format=format),
    })

"""

ORDER VIEWS

"""

@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def order_list(request, format=None):
    
    """List all orders or create new."""
    
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def order_detail(request, pk, format=None):

    """Read, update, delete an order"""
    
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""

RETAILER VIEWS

"""

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def retailer_list(request, format=None):
    
    """List all retailers or create new."""
    
    if request.method == 'GET':
        retailers = Retailer.objects.all()
        serializer = RetailerSerializer(retailers, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RetailerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def retailer_detail(request, pk, format=None):

    """Read, update, delete a retailer"""
    
    try:
        retailer = Retailer.objects.get(pk=pk)
    except Retailer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = RetailerSerializer(retailer)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = RetailerSerializer(retailer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        serializer = RetailerSerializer(retailer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        retailer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""

SUPPLIER VIEWS 

"""

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def supplier_list(request, format=None):
    
    """List all suppliers or create new."""
    
    if request.method == 'GET':
        suppliers = Supplier.objects.all()
        serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def supplier_detail(request, pk, format=None):

    """Read, update, delete a supplier"""
    
    try:
        supplier = Supplier.objects.get(pk=pk)
    except supplier.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = SupplierSerializer(supplier)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SupplierSerializer(supplier, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        supplier.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""

CONCESSION VIEWS

"""

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def concession_list(request, format=None):
    
    """List all concessions or create new."""
    
    if request.method == 'GET':
        concessions = Concession.objects.all()
        serializer = ConcessionSerializer(concessions, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ConcessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def concession_detail(request, pk, format=None):

    """Read, update, delete a concession"""
    
    try:
        concession = Concession.objects.get(pk=pk)
    except Concession.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ConcessionSerializer(concession)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ConcessionSerializer(concession, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        serializer = ConcessionSerializer(concession, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        concession.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""

CONCESSION MEMO VIEWS

"""

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def memo_list(request, format=None):
    
    """List all memos or create new."""
    
    if request.method == 'GET':
        memos = Memo.objects.all()
        serializer = MemoSerializer(memos, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MemoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def memo_detail(request, pk, format=None):

    """Read, update, delete a memo"""
    
    try:
        memo = Memo.objects.get(pk=pk)
    except Memo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = MemoSerializer(memo)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = MemoSerializer(memo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        serializer = MemoSerializer(memo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        memo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""

MANUAL ORDER VIEWS

"""

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def manual_list(request, format=None):
    
    """List all manual orders or create new."""
    
    if request.method == 'GET':
        manuals = ManualOrder.objects.all()
        serializer = ManualOrderSerializer(manuals, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ManualOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def manual_detail(request, pk, format=None):

    """Read, update, delete a manual order"""
    
    try:
        manual = ManualOrder.objects.get(pk=pk)
    except Manual.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ManualSerializer(manual)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ManualSerializer(manual, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        serializer = ManualSerializer(manual, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        manual.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)