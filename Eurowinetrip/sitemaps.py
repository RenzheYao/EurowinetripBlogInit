from django.contrib.sitemaps import Sitemap
from .models import BlogPost

class PostSitemap(Sitemap):
    # These tell bots how often to come back
    changefreq = "weekly"
    priority = 0.8  # Importance scale from 0.1 to 1.0

    def items(self):
        # Only index posts that are actually published
        # Adjust 'status' to whatever field name you use for publishing logic
        return BlogPost.objects.filter(status='published').order_by('-publish_date')

    def lastmod(self, obj):
        # Crucial for AI: Tells them when you last updated the content
        return obj.updated_at

    def location(self, obj):
        # IMPORTANT: This must match your React Frontend URL structure
        return f"/post/{obj.slug}"