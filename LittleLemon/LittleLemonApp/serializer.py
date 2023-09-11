from rest_framework import serializers
from .models import Category,MenuItems,Cart,Order,OrderItem
from django.contrib.auth.models import User

# class CategorySerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug','title']

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = MenuItems
        fields = ['id','title','price','featured','category','category_id']

class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)

    unit_price = serializers.DecimalField(max_digits=6,decimal_places=2,read_only=True)
    price = serializers.DecimalField(max_digits=6,decimal_places=2,read_only=True)

    class Meta:
        model = Cart
        fields = ['id','user','menuitem','quantity','unit_price','price','menuitem_id']

    def create(self, validated_data):
        menuitem_id = validated_data.get('menuitem_id')
        menuitem_price = MenuItems.objects.get(id=menuitem_id).price
        validated_data['unit_price'] = menuitem_price
        validated_data['price'] = menuitem_price * validated_data['quantity']
        return super().create(validated_data)

class OrderSerializer(serializers.ModelSerializer):
    delivery_crew = UserSerializer(read_only=True)
    delivery_crew_id = serializers.IntegerField(write_only=True,required=False)
    class Meta:
        model = Order
        fields = ['id','user','delivery_crew','status','total','date','delivery_crew_id']

class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    order_id = serializers.IntegerField(write_only=True)
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = OrderItem
        fields = ['id','order','menuitem','quantity','unit_price','price','order_id','menuitem_id']