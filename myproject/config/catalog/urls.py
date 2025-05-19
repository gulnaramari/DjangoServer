from .apps import CatalogConfig
from django.urls import path
from . import views


app_name = CatalogConfig.name


urlpatterns = [
    path('home/', views.ContactsView.as_view(), name='home'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('', views.ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name="product_detail"),
    path('add_product/', views.ProductCreateView.as_view(), name="add_product"),
    path('product/<int:pk>/update/', views.ProductUpdateView.as_view(), name='update_product'),
    path('product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='delete_product'),
]
