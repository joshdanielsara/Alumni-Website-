from django.db import models
from django.contrib.auth.models import User

# Post Models
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', through='Like')
    photo = models.ImageField(upload_to='post_photos/', null=True, blank=True)
    video = models.FileField(upload_to='post_videos/', null=True, blank=True)
    category_choices = [('Jobs', 'Jobs'), ('Events', 'Events'), ('News', 'News')]
    category = models.CharField(max_length=50, choices=category_choices, default='Events') 
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

# Like Model
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'post']

# Comment Model
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

# Message Models
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} to {self.receiver} - {self.timestamp}"

# Group Models
class Group(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name



class Message(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.sender.first_name}: {self.content}"


# Profile Models
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    year_graduated = models.CharField(max_length=4)
    strand = models.CharField(max_length=10, choices=[
        ('tvl', 'TVL'),
        ('abm', 'ABM'),
        ('humss', 'HUMSS'),
        ('stem', 'STEM'),
    ])
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username

# UserProfile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    year_graduated = models.CharField(max_length=30, blank=True, null=True)
    strand = models.CharField(max_length=10, blank=True, null=True, choices=[
        ('tvl', 'TVL'),
        ('abm', 'ABM'),
        ('humss', 'HUMSS'),
        ('stem', 'STEM'),
    ])
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.user.username