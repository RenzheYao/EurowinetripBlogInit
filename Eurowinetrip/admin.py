from django.contrib import admin
from .models import Category, Tag, BlogPost, PostImage, Comment, ContactMessage

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1
    # Added alt text fields for gallery image AI recognition
    fields = ['image', 'alt_text_en', 'alt_text_zh', 'caption', 'order']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_zh', 'name_en', 'slug', 'order')
    prepopulated_fields = {'slug': ('name_en',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name_zh', 'name_en', 'slug')
    prepopulated_fields = {'slug': ('name_en',)}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    # Display key metrics and status in the list view
    list_display = ('title_en', 'category', 'status', 'geo_placename', 'is_featured', 'publish_date', 'view_count')
    list_filter = ('status', 'category', 'is_featured', 'publish_date')
    search_fields = ('title_zh', 'title_en', 'geo_placename', 'key_entities')
    prepopulated_fields = {'slug': ('title_en',)}
    inlines = [PostImageInline]
    
    fieldsets = (
        ('Publishing Status', {
            'fields': ('status', 'publish_date', 'is_featured', 'view_count', 'read_time_minutes')
        }),
        ('English Content', {
            'fields': ('title_en', 'excerpt_en', 'content_en')
        }),
        ('Chinese Content', {
            'fields': ('title_zh', 'excerpt_zh', 'content_zh')
        }),
        ('Media & Taxonomy', {
            'fields': ('cover_image', 'category', 'tags', 'related_posts')
        }),
        # --- NEW SECTION: GENERATIVE AI OPTIMIZATION ---
        ('AI Optimization (GAIEO)', {
            'description': "Data for AI engines (Baidu Ernie, Google Gemini). Helps in getting cited by AI agents.",
            'fields': (
                'ai_summary_en', 
                'ai_summary_zh', 
                'key_entities', 
                'cover_image_alt_en', 
                'cover_image_alt_zh'
            ),
        }),
        ('SEO Metadata', {
            'classes': ('collapse',), 
            'fields': ('seo_title_en', 'seo_title_zh', 'seo_description_en', 'seo_description_zh', 'slug'),
        }),
        ('Geographic SEO', {
            'classes': ('collapse',),
            'fields': ('geo_region', 'geo_placename', 'geo_icbm'),
            'description': "ISO codes and coordinates for map-based search results."
        }),
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'post', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Mark selected comments as approved"
    
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('created_at',)