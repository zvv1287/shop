from django.urls import path

from adminapp import views

app_name = 'adminapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('admins-read/<str:model>/', views.AdminListView.as_view(), name='admins_read'),
    path('admins-create/<str:model>/', views.AdminCreateView.as_view(), name='admins_create'),
    path('admins-update/<str:model>/<int:pk>/', views.AdminUpdateView.as_view(), name='admins_update'),
    path('admins-delete/<str:model>/<int:pk>/', views.AdminDeleteView.as_view(), name='admins_delete'),

    path('admins-orders-read/', views.OrderList.as_view(), name='admin_orders_read'),
    path('admins-orders-update/<int:pk>/', views.AdminOrderItemsUpdate.as_view(), name='admin_order_update'),
    path('admins-orders-delet/<int:pk>/', views.AdminOrderDelete.as_view(), name='admin_order_delete'),
]
