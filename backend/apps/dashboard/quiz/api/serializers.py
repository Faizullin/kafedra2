from rest_framework import serializers

from apps.quizzes.models import Quiz, QuestionGroup, QuizQuestion, QuestionAnswer
from apps.quizzes.question.type.choice.models import MultipleChoiceOptions
from lms.core.compat import get_user_model

User = get_user_model()


class QuizAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", ]


class QuizSerializer(serializers.ModelSerializer):
    author = QuizAuthorSerializer(read_only=True)

    class Meta:
        model = Quiz
        fields = "__all__"


class QuestionGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionGroup
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = "__all__"


class MCQTypeOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleChoiceOptions
        fields = "__all__"


class MultiAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = "__all__"
