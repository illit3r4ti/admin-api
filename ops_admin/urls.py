from django.urls import path, include
from ops_admin import views

urlpatterns = [
    path('', views.api_root),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('orders/', views.order_list, name='order-list'),
    path('orders/<int:pk>/', views.order_detail, name='order-detail'),
    path('retailers/', views.retailer_list, name='retailer-list'),
    path('retailers/<int:pk>', views.retailer_detail, name='retailer-detail'),
    path('suppliers/', views.supplier_list, name='supplier-list'),
    path('suppliers/<int:pk>', views.supplier_detail, name='supplier-detail'),
    path('concessions/', views.concession_list, name='concession-list'),
    path('concessions/<int:pk>', views.concession_detail, name='concession-detail'),
    path('memos/', views.memo_list, name='memo-list'),
    path('memos/<int:pk>', views.memo_detail, name='memo-detail'),
    path('manual/', views.manual_list, name='manual-list'),
    path('manual/<int:pk>', views.manual_detail, name='manual-detail'),
]