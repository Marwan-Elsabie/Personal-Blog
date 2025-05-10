from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import uuid
from PIL import Image
# Create your models here.

class Post(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images', blank=True, null=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def like_count(self):
        return self.likes.count()

    def is_liked_by_user(self, user):
        """Check if the post is liked by a specific user."""
        return self.likes.filter(user=user).exists()  

    def toggle_like(self, user):
        """Toggle like status for a user."""
        like, created = Like.objects.get_or_create(user=user, post=self)
        if not created:
            like.delete()
            return False  # Like removed
        return True  # Like added

class Comment(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk})
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(
        upload_to='profile_pics/',
        default='profile_pics/default.png'  # Changed to .png
    )
    website = models.URLField(blank=True)
    joined_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)
        if self.profile_pic.name != 'profile_pics/default.png':
            
            try:
                img = Image.open(self.profile_pic.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.profile_pic.path)
            except:
                pass
        else:
            super().save(*args, **kwargs)

    @property
    def get_posts_count(self):
        return self.user.post_set.count()
    
    @property
    def get_comments_count(self):
        return self.user.comment_set.count()
    
    def follower_count(self):
        return self.user.followers.count()

    def following_count(self):
        return self.user.following.count()

    def is_followed_by(self, user):
        return self.user.followers.filter(follower=user).exists()
    
    def unread_notifications_count(self):
        return self.user.notifications.filter(read=False).count()
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"
    
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  # Prevent duplicate follow relationships

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
    
class Bookmark(models.Model):
    user = models.ForeignKey(User, related_name='bookmarks', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='bookmarked_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Prevent duplicate bookmarks
    
class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('follow', 'Follow'),
    )

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username} {self.get_notification_type_display()} - {self.recipient.username}"