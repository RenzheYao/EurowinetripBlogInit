from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('comments/create/', views.CommentCreateView.as_view(), name='comment-create'),
    path('comments/', views.CommentListView.as_view(), name='comment-list'),
    path('contact/', views.ContactCreateView.as_view(), name='contact-create'),
]