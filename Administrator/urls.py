# Liu Chao 
# 入    门
# 开发时间：2021/11/19 22:50
from django.urls import path
from . import views


urlpatterns = [
    path('',views.admin_view),
    path('logout',views.logout),

    path('customer',views.cus),
    path('customer/add_info',views.input_cus_info),
    # path('customer/search_info',views.search_cus_info),
    path('customer/alter_info',views.alter_cus_info),

    path('suppier',views.suppier),
    path('suppier/add_info',views.input_sup_info),
    # path('suppier/search_info',views.search_sup_info),
    path('suppier/alter_info',views.alter_sup_info),

    path('agent',views.Agent),
    path('agent/add_info',views.input_age_info),
    # path('agent/search_info',views.search_age_info),
    path('agent/alter_info',views.alter_age_info),

    path('inventory',views.invent),
    path('inventory/supply_info',views.supply_info),
    path('inventory/storage_info',views.storage_info),
    # path('inventory/alter_supply_info',views.alter_supply_info),
    path('inventory/type_info',views.type_info),

    path('sell',views.sell),
    # path('sell/retail_sale',views.retail_sale),
    # path('sell/bulk_sale',views.bulk_sale),

    path('product',views.product),
    path('product/add_alter',views.add_alter_product),
    # path('product/alter_info',views.alter_productinfo),
    path('product/release',views.search_release),

    path('booking_info',views.booking),
]