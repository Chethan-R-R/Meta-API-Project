from django.urls import path
from . import views

urlpatterns = [
    path('category',views.category),
    path('menu-items',views.menu_items),
    path('menu-item/<int:item_id>',views.menu_item),
    path('groups/manager/users',views.managers),
    path('groups/manager/users/<int:id>',views.manager),
    path('groups/delivery-crew/users',views.delivery_crew),
    path('groups/delivery-crew/users/<int:id>',views.delivery_person),
    path('cart/menu-items',views.cart),
    path('orders',views.orders),
    path('orders/<int:id>',views.order)
]