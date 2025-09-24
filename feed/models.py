
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import uuid

def cuid():
    return uuid.uuid4().hex

class UserManager(BaseUserManager):
    def create_user(self, email, username, name, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, username, name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=32, primary_key=True, default=cuid, editable=False)
    name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    avatar = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    posts_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "name"]

    objects = UserManager()

    def __str__(self):
        return self.username

class Post(models.Model):
    id = models.CharField(max_length=32, primary_key=True, default=cuid, editable=False)
    content = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=["author"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return f"{self.author.username}: {self.content[:30]}"

class Media(models.Model):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    MEDIA_TYPE_CHOICES = [(IMAGE, "Image"), (VIDEO, "Video")]

    id = models.CharField(max_length=32, primary_key=True, default=cuid, editable=False)
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="media")
    type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    url = models.URLField()
    thumbnail = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    id = models.CharField(max_length=32, primary_key=True, default=cuid, editable=False)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    likes_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

class PostLike(models.Model):
    id = models.CharField(max_length=32, primary_key=True, default=cuid, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ("user", "post")

class CommentLike(models.Model):
    id = models.CharField(max_length=32, primary_key=True, default=cuid, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_likes")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ("user", "comment")

class PostShare(models.Model):
    id = models.CharField(max_length=32, primary_key=True, default=cuid, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shares")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="shares_on_post")
    shared_at = models.DateTimeField(auto_now_add=True)
