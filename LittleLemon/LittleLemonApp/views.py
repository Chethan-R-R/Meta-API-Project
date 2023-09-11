from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Category,MenuItems,Cart,Order,OrderItem
from .serializer import CategorySerializer,MenuItemSerializer,UserSerializer,CartSerializer,OrderSerializer,OrderItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User,Group

# Category endpoints
@api_view(['GET','POST'])
def category(req):
    if req.method == 'GET':
        categories = Category.objects.all()
        serialized_category = CategorySerializer(categories,many=True)
        return Response(serialized_category.data,status=status.HTTP_200_OK)

    if req.method == 'POST':
        if req.user.groups.filter(name='Manager').exists():
            serialized_data = CategorySerializer(data=req.data)
            serialized_data.is_valid(raise_exception=True)
            serialized_data.save()
            return Response(serialized_data.data,status=status.HTTP_200_OK)

# Menu-items endpoints

@api_view(['GET','POST'])
def menu_items(req):
    if req.method == 'GET':
        menuitems = MenuItems.objects.all()
        serialized_menuitems = MenuItemSerializer(menuitems,many=True)
        return Response(serialized_menuitems.data,status=status.HTTP_200_OK)
    if req.method == 'POST':
        if req.user.groups.filter(name='Manager').exists():
            serialized_data = MenuItemSerializer(data=req.data)
            serialized_data.is_valid(raise_exception=True)
            serialized_data.save()
            return Response(serialized_data.data,status=status.HTTP_200_OK)

@api_view(['GET','PUT','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def menu_item(req,item_id):
    if req.method == 'GET':
        menuitem = MenuItems.objects.get(pk=item_id)
        serialized_menuitem = MenuItemSerializer(menuitem)
        return Response(serialized_menuitem.data,status=status.HTTP_200_OK)
    if req.method in ('PUT','PATCH'):
        if req.user.groups.filter(name='Manager').exists():
            menuitem =MenuItems.objects.get(pk=item_id)
            serialized_data = MenuItemSerializer(menuitem,data=req.data,partial= req.method == 'PATCH')
            serialized_data.is_valid(raise_exception=True)
            serialized_data.save()
            return Response(serialized_data.data,status=status.HTTP_202_ACCEPTED)
        return Response({"error":"not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    if req.method == 'DELETE':
        if req.user.groups.filter(name='Manager').exists():
            menuitem = MenuItems.objects.get(pk = 1)
            menuitem.delete()
            return Response('menu item deleted',status=status.HTTP_204_NO_CONTENT)
        return Response({"error":"not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)

# User group management endpoints

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def managers(req):
    if req.user.groups.filter(name='Manager').exists():
        if req.method == 'GET':
            manager_group = Group.objects.get(name="Manager")
            managers = User.objects.filter(groups=manager_group)
            serialized_managers = UserSerializer(managers,many=True)
            return Response(serialized_managers.data,status=status.HTTP_200_OK)
        if req.method == 'POST':
            username = req.data['username']
            if username:
                manager_group = Group.objects.get(name='Manager')
                try:
                    user = User.objects.get(username=username)
                    manager_group.user_set.add(user)
                    return Response({'message':'ok'},status=status.HTTP_202_ACCEPTED)
                except:
                    return Response({'message':'error'},status=status.HTTP_404_NOT_FOUND)
            return Response({'message':'error'},status=status.HTTP_404_NOT_FOUND)
    return Response({"error":"not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def manager(req,id):
    if req.user.groups.filter(name='Manager').exists():
        manager_group = Group.objects.get(name='Manager')
        try:
            user = User.objects.get(id=id)
            manager_group.user_set.remove(user)
            return Response({'message':'ok'},status=status.HTTP_202_ACCEPTED)
        except:
            return Response({'message':'error'},status=status.HTTP_404_NOT_FOUND)
    return Response({"error":"not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def delivery_crew(req):
    if req.user.groups.filter(name='Manager').exists():
        if req.method == 'GET':
            delivery_group = Group.objects.get(name='Delivery crew')
            delivery_crew = User.objects.filter(groups=delivery_group)
            serialized_data = UserSerializer(delivery_crew,many=True)
            return Response(serialized_data.data,status=status.HTTP_200_OK)
        elif req.method == 'POST':
            username = req.data['username']
            if username:
                delivery_group = Group.objects.get(name='Delivery crew')
                try:
                    user = User.objects.get(username=username)
                    delivery_group.user_set.add(user)
                    return Response({'message':'ok'},status=status.HTTP_202_ACCEPTED)
                except:
                    return Response({'message':'error'},status=status.HTTP_404_NOT_FOUND)
            return Response({'message':'error'},status=status.HTTP_404_NOT_FOUND)
    return Response({"error":"not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delivery_person(req,id):
    if req.user.groups.filter(name='Manager').exists():
        delivery_group = Group.objects.get(name='Delivery crew')
        try:
            user = User.objects.get(id=id)
            delivery_group.user_set.remove(user)
            return Response({'message':'ok'},status=status.HTTP_202_ACCEPTED)
        except:
            return Response({'message':'error'},status=status.HTTP_404_NOT_FOUND)
    return Response({"error":"not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)

# Cart management endpoints

@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def cart(req):
    if req.method == 'GET':
        cart_list = Cart.objects.filter(user=req.user)
        serialized_cart = CartSerializer(cart_list,many=True)
        return Response(serialized_cart.data,status=status.HTTP_200_OK)
    elif req.method == 'POST':
        req.data['user'] = req.user.id
        serialized_cart = CartSerializer(data=req.data)
        serialized_cart.is_valid(raise_exception=True)
        serialized_cart.save()
        return Response(serialized_cart.data,status=status.HTTP_201_CREATED)
    elif req.method == 'DELETE':
        Cart.objects.filter(user=req.user).delete()
        return Response({'message': 'All cart items deleted'}, status=status.HTTP_204_NO_CONTENT)

# Order management endpoints
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def orders(req):
    if req.method == 'GET':
        if req.user.groups.filter(name='Manager').exists():
            customer_orders = OrderItem.objects.all()
            serialized_customer_order = OrderItemSerializer(customer_orders,many=True)
            return Response(serialized_customer_order.data,status=status.HTTP_200_OK)
        elif req.user.groups.filter(name='Delivery crew').exists():
            order_items = []
            customer_orders = Order.objects.filter(delivery_crew=req.user.id)
            for order in customer_orders:
                order_item = OrderItem.objects.filter(order=order.id)
                order_items+=order_item
            serialized_customer_order = OrderItemSerializer(order_items,many=True)
            return Response(serialized_customer_order.data,status=status.HTTP_200_OK)
        else:
            order_items = []
            customer_orders = Order.objects.filter(user=req.user)
            for order in customer_orders:
                order_item = OrderItem.objects.filter(order=order.id)
                order_items+=order_item
            serialized_customer_order = OrderItemSerializer(order_items,many=True)
            return Response(serialized_customer_order.data,status=status.HTTP_200_OK)
    if req.method == 'POST':
        user = req.user
        cart_list = Cart.objects.filter(user=user)
        total = 0
        for item in cart_list:
            total+=item.price
        serialized_customer_order = OrderSerializer(data={"user":user.id,"total":total})
        serialized_customer_order.is_valid(raise_exception=True)
        saved_order = serialized_customer_order.save()
        for item in cart_list:
            data = {
                'order_id' : saved_order.id,
                'menuitem_id':item.menuitem.id,
                'quantity':item.quantity,
                'unit_price':item.unit_price,
                'price':item.price
            }
            serialized_order_item = OrderItemSerializer(data=data)
            serialized_order_item.is_valid(raise_exception=True)
            serialized_order_item.save()
            Cart.objects.filter(user=req.user).delete()
        return Response(serialized_customer_order.data,status=status.HTTP_201_CREATED)
    return Response({"error":"not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET','PUT','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def order(req,id):
    if req.method == 'GET':
        if req.user.groups.filter(name='Manager').exists():
            order_items = OrderItem.objects.filter(order=id)
            serialized_items = OrderItemSerializer(order_items,many=True)
            return Response(serialized_items.data,status=status.HTTP_200_OK)
        else:
            order = Order.objects.get(id=id)
            if order.user==req.user:
                order_items = OrderItem.objects.filter(order=id)
                serialized_items = OrderItemSerializer(order_items,many=True)
                return Response(serialized_items.data,status=status.HTTP_200_OK)
    elif req.method in ('PATCH','PUT'):
        if req.user.groups.filter(name='Manager').exists():
            order = Order.objects.get(id=id)
            serialized_order=OrderSerializer(order,data=req.data,partial=req.method=='PATCH')
            serialized_order.is_valid()
            serialized_order.save()
            return Response(serialized_order.data,status=status.HTTP_202_ACCEPTED)
        elif req.user.groups.filter(name='Delivery crew').exists():
            order = Order.objects.get(id=id)
            serialized_order=OrderSerializer(order,{"status":req.data["status"]},partial=req.method=='PATCH')
            serialized_order.is_valid()
            serialized_order.save()
            return Response(serialized_order.data,status=status.HTTP_202_ACCEPTED)
    elif req.method == 'DELETE':
        if req.user.groups.filter(name='Manager').exists():
            OrderItem.objects.filter(order=id).delete()
            Order.objects.get(id=id).delete()
            return Response({"message":"order deleted"},status=status.HTTP_202_ACCEPTED)
    return Response({"error":"not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)