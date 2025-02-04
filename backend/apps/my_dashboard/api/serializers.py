from rest_framework import serializers

from apps.posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
