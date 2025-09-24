import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from django.db import transaction, models
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from .models import User, Post, PostLike, Comment

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "name", "email", "avatar", "bio", "posts_count")

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("id", "content", "author", "created_at", "likes_count", "comments_count", "shares_count")
class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = "__all__"

class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    post = graphene.Field(PostType, id=graphene.String(required=True))
    posts = graphene.List(PostType, first=graphene.Int(), after=graphene.String())

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            return None
        return user

    def resolve_post(self, info, id):
        return Post.objects.filter(id=id).first()

    def resolve_posts(self, info, first=10, after=None):
        qs = Post.objects.select_related("author").order_by("-created_at")
        # simple offset/limit pagination for now; replace with cursor-based as needed
        return qs[:first]

class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        content = graphene.String(required=True)

    @login_required
    def mutate(self, info, content):
        user = info.context.user
        post = Post.objects.create(content=content, author=user)
        # increment user's posts_count
        User.objects.filter(pk=user.pk).update(posts_count=models.F('posts_count') + 1)
        return CreatePost(post=post)

class LikePost(graphene.Mutation):
    ok = graphene.Boolean()
    likes_count = graphene.Int()

    class Arguments:
        post_id = graphene.String(required=True)

    @login_required
    def mutate(self, info, post_id):
        user = info.context.user
        post = Post.objects.filter(id=post_id).first()
        if not post:
            raise Exception("Post not found")
        obj, created = PostLike.objects.get_or_create(user=user, post=post)
        if created:
            # atomic increment
            with transaction.atomic():
                Post.objects.filter(pk=post.pk).update(likes_count=models.F('likes_count') + 1)
            return LikePost(ok=True, likes_count=post.likes_count + 1)
        return LikePost(ok=False, likes_count=post.likes_count)

class CreateComment(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)
        content = graphene.String(required=True)

    comment = graphene.Field(lambda: CommentType)

    @classmethod
    def mutate(cls, root, info, post_id, content):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Authentication required")

        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise GraphQLError("Post not found")

        comment = Comment.objects.create(
            post=post,
            author=user,
            content=content
        )
        return CreateComment(comment=comment)


class UpdatePost(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)
        content = graphene.String(required=True)

    post = graphene.Field(lambda: PostType)

    @classmethod
    def mutate(cls, root, info, post_id, content):
        user = info.context.user
        try:
            post = Post.objects.get(pk=post_id, author=user)
        except Post.DoesNotExist:
            raise GraphQLError("Post not found or not yours")

        post.content = content
        post.save()
        return UpdatePost(post=post)

class UnlikePost(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, post_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Authentication required")

        try:
            like = PostLike.objects.get(post_id=post_id, user=user)
        except PostLike.DoesNotExist:
            raise GraphQLError("You haven’t liked this post")

        like.delete()
        return UnlikePost(ok=True)



class DeletePost(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, post_id):
        user = info.context.user
        try:
            post = Post.objects.get(pk=post_id, author=user)
        except Post.DoesNotExist:
            raise GraphQLError("Post not found or not yours")

        post.delete()
        return DeletePost(ok=True)


class AuthMutations(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


class Mutation(AuthMutations, graphene.ObjectType):
    create_post = CreatePost.Field()
    like_post = LikePost.Field()
    unlike_post = UnlikePost.Field() 
    create_comment = CreateComment.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
schema = graphene.Schema(query=Query, mutation=Mutation)
