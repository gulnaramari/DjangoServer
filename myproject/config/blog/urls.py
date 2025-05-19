from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('home/', views.PostsListView.as_view(), name='home'),
    path('post/<int:pk>/', views.PostDetailsView.as_view(), name='post_details'),
    path('add_post/', views.PostCreateView.as_view(), name='add_post'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='update_post'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete_post'),
]

