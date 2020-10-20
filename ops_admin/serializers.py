from rest_framework import serializers
from ops_admin.models import Order, Retailer, Supplier, Concession, Memo, ManualOrder
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    orders = serializers.PrimaryKeyRelatedField(many=True, queryset=Order.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'orders', 'retailers', 'suppliers', 'concessions', 'memos', 'manuals']

class OrderSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    recieved = serializers.DateTimeField()
    supplier = serializers.CharField(max_length=4, required=False, allow_blank=True, default='')
    retailer = serializers.CharField(max_length=4, required=False, allow_blank=True, default='')
    ordernum = serializers.CharField(max_length=20, required=False, allow_blank=True, default='')

    def create(self, validated_data):

        """Create and return a new Order instance when passed validated_data"""

        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):

        """Update and return an existing Order instance when passed validated_data"""

        instance.supplier = validated_data.get('supplier', instance.supplier)
        instance.retailer = validated_data.get('retailer', instance.retailer)
        instance.ordernum = validated_data.get('ordernum', instance.ordernum)
        instance.save()

        return instance

class RetailerSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:

        model = Retailer
        fields = ['owner','code', 'name', 'list']

class SupplierSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')    
    
    class Meta:

        model = Supplier
        fields = ['owner','code', 'name']

class ConcessionSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:

        model = Concession
        fields = [
            'owner',
            'retailer', 
            'supplier', 
            'product', 
            'description', 
            'best_before', 
            'start_date', 
            'end_date'
            ]

class MemoSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:

        model = Memo
        fields = ['owner','retailer', 'supplier', 'start_date', 'end_date', 'content']

class ManualOrderSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:

        model = ManualOrder
        fields = ['owner','retailer', 'supplier', 'processing', 'details', 'attachments']

