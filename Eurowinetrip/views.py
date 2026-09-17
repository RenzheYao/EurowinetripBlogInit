from rest_framework import generics, filters, permissions
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F
from rest_framework.exceptions import ValidationError
from .models import BlogPost, Category, Comment, ContactMessage
from .serializers import (
    BlogPostListSerializer, BlogPostDetailSerializer, 
    CategorySerializer, CommentSerializer, ContactMessageSerializer
)

class PostListView(generics.ListAPIView):
    """
    Handles List of Posts with:
    - Pagination (from settings)
    - Filtering by Category or Tag slug
    - Ordering by publish_date/view_count
    - Search by title
    """
    queryset = BlogPost.objects.filter(status='published')
    serializer_class = BlogPostListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    
    filterset_fields = ['category__slug', 'tags__slug']
    ordering_fields = ['publish_date', 'view_count']
    ordering = ['-publish_date'] 
    search_fields = ['title_zh', 'title_en']


class PostDetailView(generics.RetrieveAPIView):
    """
    Retrieves a single post and increments the view count.
    Prioritizes SessionAuthentication to recognize logged-in Admins.
    """
    queryset = BlogPost.objects.filter(status='published')
    serializer_class = BlogPostDetailSerializer
    lookup_field = 'slug'
    
    # ADDED: Ensures Django checks your browser session for Admin status
    authentication_classes = [SessionAuthentication, JWTAuthentication, TokenAuthentication]

    def get_object(self):
        obj = super().get_object()
        
        # UPDATED: Only increment if the user is NOT a logged-in staff member
        is_staff = self.request.user.is_authenticated and self.request.user.is_staff
        
        if not is_staff:
            # Use F() to increment directly in the database to prevent race conditions
            obj.view_count = F('view_count') + 1
            obj.save(update_fields=['view_count'])
            # Refresh from DB to ensure the serializer sends back the correct updated number
            obj.refresh_from_db()
            
        return obj


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all().order_by('order')
    serializer_class = CategorySerializer
    pagination_class = None 


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        if not post_id:
            raise ValidationError({"post": "You must provide a post ID to comment."})
        serializer.save(post_id=post_id)


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post')
        if post_id is not None:
            queryset = queryset.filter(post_id=post_id)
        return queryset


class ContactCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.AllowAny]