from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField

class Category(models.Model):
    name_zh = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True) 
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ["order"]
        verbose_name_plural = "Categories"
        
    def __str__(self):
        return f"{self.name_en} | {self.name_zh}"
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en)
        super().save(*args, **kwargs)

class Tag(models.Model):
    name_zh = models.CharField(max_length=50)
    name_en = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)
    
    def __str__(self):
        return self.name_en
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en)
        super().save(*args, **kwargs)

class BlogPost(models.Model):
    DRAFT = "draft"
    PUBLISHED = "published"
    STATUS_CHOICES = [(DRAFT, "Draft"), (PUBLISHED, "Published")]
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=DRAFT)
    publish_date = models.DateTimeField(null=True, blank=True)
    
    title_zh = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200)
    
    excerpt_zh = models.TextField()
    excerpt_en = models.TextField()

    content_zh = RichTextUploadingField()
    content_en = RichTextUploadingField()
    
    # --- COVER IMAGE ENHANCEMENT ---
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)
    cover_image_alt_zh = models.CharField(max_length=200, blank=True, help_text="AI SEO: Description of the cover photo for Baidu Ernie")
    cover_image_alt_en = models.CharField(max_length=200, blank=True, help_text="AI SEO: Description of the cover photo for Google SGE")
    
     # RELATIONSHIPS
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="posts")
    tags = models.ManyToManyField(Tag, blank=True)
    related_posts = models.ManyToManyField("self", blank=True)
    
    # --- TRADITIONAL SEO FIELDS ---
    seo_title_zh = models.CharField(max_length=200, blank=True)
    seo_title_en = models.CharField(max_length=200, blank=True)
    seo_description_zh = models.CharField(max_length=300, blank=True)
    seo_description_en = models.CharField(max_length=300, blank=True)
    
    # --- GENERATIVE AI OPTIMIZATION (GAIO) ---
    ai_summary_zh = models.TextField(blank=True, help_text="Fact-based summary for Baidu Ernie Bot to cite.")
    ai_summary_en = models.TextField(blank=True, help_text="Fact-based summary for Google Gemini to cite.")
    key_entities = models.CharField(max_length=500, blank=True, help_text="Comma-separated list of entities (Region, Grape, Vintage) for AI reasoning.")

    # GEO OPTIMIZATION
    geo_region = models.CharField(max_length=10, blank=True)
    geo_placename = models.CharField(max_length=100, blank=True)
    geo_icbm = models.CharField(max_length=50, blank=True)
    
    # METADATA
    slug = models.SlugField(unique=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    read_time_minutes = models.PositiveIntegerField(default=1)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-publish_date", "-created_at"]

    def __str__(self):
        return self.title_en

    def get_absolute_url(self):
        """Standard method for Sitemaps to find the React frontend path."""
        return f"/post/{self.slug}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en)
        if self.status == self.PUBLISHED and not self.publish_date:
            self.publish_date = timezone.now()
        if self.content_en:
            # Simple read time estimation
            self.read_time_minutes = max(1, len(self.content_en) // 500)
        super().save(*args, **kwargs)

class PostImage(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="blog/gallery/")
    alt_text_zh = models.CharField(max_length=200, blank=True, help_text="Describe image for Chinese AI agents")
    alt_text_en = models.CharField(max_length=200, blank=True, help_text="Describe image for English AI agents")
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ["order"]

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="comments")
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()
    content = models.TextField()
    is_approved = models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author_name} on {self.post.title_en}"

class ContactMessage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(max_length=2000) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.first_name} {self.last_name}"