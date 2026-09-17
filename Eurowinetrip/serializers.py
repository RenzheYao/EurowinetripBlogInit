from rest_framework import serializers
from .models import Category, Tag, BlogPost, PostImage, Comment, ContactMessage

# --- BASIC SERIALIZERS ---

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        # Added Alt Text fields to support AI Image Recognition/SEO
        fields = ['image', 'caption', 'alt_text_zh', 'alt_text_en', 'order']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author_name', 'author_email', 'content', 'created_at']

# --- HELPER SERIALIZERS ---

class RelatedPostSerializer(serializers.ModelSerializer):
    """Simplified version for sidebars to prevent massive payloads"""
    class Meta:
        model = BlogPost
        fields = ['id', 'slug', 'title_zh', 'title_en', 'excerpt_zh', 'excerpt_en']

# --- MAIN POST SERIALIZERS ---

class BlogPostListSerializer(serializers.ModelSerializer):
    """Optimized for the homepage/list view (lighter weight)"""
    category_name_zh = serializers.CharField(source='category.name_zh', read_only=True)
    category_name_en = serializers.CharField(source='category.name_en', read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'id', 'slug', 'title_zh', 'title_en', 'excerpt_zh', 'excerpt_en', 
            'cover_image', 'category_name_zh', 'category_name_en', 
            'publish_date', 'is_featured', 'read_time_minutes', 'view_count',
            # Added cover image alt for AI recognition in lists
            'cover_image_alt_zh', 'cover_image_alt_en'
        ]

class BlogPostDetailSerializer(serializers.ModelSerializer):
    """The 'Heavy' serializer for the Post Detail page, now with GAIEO support"""
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    images = PostImageSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()
    related_posts = RelatedPostSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'id', 'slug', 'status', 'publish_date', 'title_zh', 'title_en', 
            'excerpt_zh', 'excerpt_en', 'content_zh', 'content_en', 
            'cover_image', 'category', 'tags', 'related_posts', 
            'images', 'comments', 'view_count', 'read_time_minutes',
            'is_featured', 'created_at', 'updated_at',
            
            # --- COVER IMAGE & SEO ---
            'cover_image', 'cover_image_alt_zh', 'cover_image_alt_en',
            
            # --- AI COMPLIANCE FIELDS (NEW) ---
            'is_ai_generated', 'is_ai_polished',
            
            # --- GENERATIVE AI OPTIMIZATION (GAIEO) FIELDS ---
            'ai_summary_zh', 'ai_summary_en', 
            'key_entities',
            'cover_image_alt_zh', 'cover_image_alt_en',

            # --- BACKEND SEO FIELDS ---
            'seo_title_zh', 'seo_title_en', 
            'seo_description_zh', 'seo_description_en',

            # --- BACKEND GEO FIELDS ---
            'geo_region', 'geo_placename', 'geo_icbm'
        ]

    def get_comments(self, obj):
        # Only sends approved comments to the frontend
        approved_comments = obj.comments.filter(is_approved=True)
        return CommentSerializer(approved_comments, many=True).data

# --- UTILITY SERIALIZERS ---

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'phone', 'city', 'message']