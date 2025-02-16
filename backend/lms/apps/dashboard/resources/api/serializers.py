from rest_framework import serializers

from lms.core.compat import get_user_model
from lms.core.loading import get_model

Post = get_model("posts", "Post")
Category = get_model("posts", "Category")
Tag = get_model("posts", "Tag")
User = get_user_model()


class PostAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "term", "description", "created_at", "updated_at"]


class PostSerializer(serializers.ModelSerializer):
    author = PostAuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "author", "category", "created_at", "updated_at", "publication_status", "meta_title"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "title", ]
#
# class CourseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = "__all__"
#
#
# class QuizSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = "__all__"
