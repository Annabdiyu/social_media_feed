import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from django.db import transaction, models
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from .models import User, Post, PostLike, Comment

# ----------------------
# GraphQL Types
# ----------------------

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email", "posts_count")

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("id", "author", "content", "likes_count", "comments_count", "shares_count", "created_at", "updated_at")

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ("id", "post", "author", "content", "created_at")


# ----------------------
# Mutations
# ----------------------

class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        content = graphene.String(required=True)

    @login_required
    def mutate(self, info, content):
        user = info.context.user
        post = Post.objects.create(author=user, content=content)
        # Increment user post count
        User.objects.filter(pk=user.pk).update(posts_count=models.F('posts_count') + 1)
        return CreatePost(post=post)


class UpdatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        post_id = graphene.ID(required=True)
        content = graphene.String(required=True)

    @login_required
    def mutate(self, info, post_id, content):
        user = info.context.user
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise GraphQLError("Post not found")
        if post.author != user:
            raise GraphQLError("Not authorized to update this post")
        post.content = content
        post.save()
        return UpdatePost(post=post)


class DeletePost(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        post_id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, post_id):
        user = info.context.user
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise GraphQLError("Post not found")
        if post.author != user:
            raise GraphQLError("Not authorized to delete this post")
        with transaction.atomic():
            post.delete()
            User.objects.filter(pk=user.pk).update(posts_count=models.F('posts_count') - 1)
        return DeletePost(ok=True)


class LikePost(graphene.Mutation):
    likes_count = graphene.Int()
    ok = graphene.Boolean()

    class Arguments:
        post_id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, post_id):
        user = info.context.user
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise GraphQLError("Post not found")
        # Check if already liked
        if PostLike.objects.filter(post=post, user=user).exists():
            raise GraphQLError("Already liked")
        with transaction.atomic():
            PostLike.objects.create(post=post, user=user)
            Post.objects.filter(pk=post_id).update(likes_count=models.F('likes_count') + 1)
        post.refresh_from_db()
        return LikePost(ok=True, likes_count=post.likes_count)


class UnlikePost(graphene.Mutation):
    likes_count = graphene.Int()
    ok = graphene.Boolean()

    class Arguments:
        post_id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, post_id):
        user = info.context.user
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise GraphQLError("Post not found")
        like = PostLike.objects.filter(post=post, user=user).first()
        if not like:
            raise GraphQLError("You haven't liked this post")
        with transaction.atomic():
            like.delete()
            Post.objects.filter(pk=post_id).update(likes_count=models.F('likes_count') - 1)
        post.refresh_from_db()
        return UnlikePost(ok=True, likes_count=post.likes_count)


class CreateComment(graphene.Mutation):
    comment = graphene.Field(CommentType)

    class Arguments:
        post_id = graphene.ID(required=True)
        content = graphene.String(required=True)

    @login_required
    def mutate(self, info, post_id, content):
        user = info.context.user
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise GraphQLError("Post not found")
        comment = Comment.objects.create(post=post, author=user, content=content)
        Post.objects.filter(pk=post_id).update(comments_count=models.F('comments_count') + 1)
        return CreateComment(comment=comment)


class SharePost(graphene.Mutation):
    shares_count = graphene.Int()
    ok = graphene.Boolean()

    class Arguments:
        post_id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, post_id):
        user = info.context.user
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise GraphQLError("Post not found")

        # Increment shares count
        with transaction.atomic():
            Post.objects.filter(pk=post_id).update(shares_count=models.F('shares_count') + 1)
        
        post.refresh_from_db()
        return SharePost(ok=True, shares_count=post.shares_count)



# ----------------------
# Queries
# ----------------------

class Query(graphene.ObjectType):
    posts = graphene.List(PostType, first=graphene.Int())
    post = graphene.Field(PostType, post_id=graphene.ID(required=True))

    def resolve_posts(self, info, first=None):
        qs = Post.objects.all().order_by('-created_at')
        if first:
            qs = qs[:first]
        return qs

    def resolve_post(self, info, post_id):
        try:
            return Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise GraphQLError("Post not found")


# ----------------------
# Mutations Root
# ----------------------

class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
    like_post = LikePost.Field()
    unlike_post = UnlikePost.Field()
    create_comment = CreateComment.Field()
    share_post = SharePost.Field()
    # JWT Auth
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
