from rest_framework import serializers

from lms.core.compat import get_user_model
from lms.core.loading import get_model

Post = get_model("posts", "Post")
Category = get_model("posts", "Category")
User = get_user_model()


class PostAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", ]


class PostSerializer(serializers.ModelSerializer):
    author = PostAuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"

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
