from utils.serializers import TimestampedSerializer, serializers
from .models import Post, UserModel, PostComment, PostCategory


class PostAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        exclude = ('id', 'username', 'first_name', 'last_name')


class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        exclude = ('id', 'slug', 'title')


class PostListSerializer(serializers.ModelSerializer):
    category = PostCategorySerializer(read_only=True)
    author = PostAuthorSerializer(read_only=True)

    class Meta:
        model = Post
        exclude = ('id', 'slug', 'status', 'author', 'category')


class PostRetrieveSerializer(TimestampedSerializer):
    category = PostCategorySerializer(read_only=True)
    author = PostAuthorSerializer(read_only=True)

    class Meta:
        model = Post
        exclude = ('id', 'slug', 'status', 'author', 'category', 'content', 'created_at', 'updated_at')


class PostCommentSerializer(TimestampedSerializer):
    author = PostAuthorSerializer(read_only=True)

    class Meta:
        model = PostComment
        fields = ('id', 'author', 'title', 'message', 'created_at', 'updated_at')
