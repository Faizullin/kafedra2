from django.utils.timezone import override
from django_filters import CharFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import generics, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from apps.quizzes.models import Quiz, QuestionGroup, QuizQuestion, QuestionType
from utils.api_actions import BaseAction, BaseActionException
from .filters import CustomPagination
from .serializers import QuizSerializer, QuestionGroupSerializer, QuestionSerializer, MCQTypeOptionsSerializer, \
    MultiAnswerSerializer


class BaseListApiView(generics.ListAPIView):
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['id', 'created_at', 'updated_at']
    filterset_class = None


class BaseDestroyApiView(generics.DestroyAPIView):
    lookup_field = "id"


##########################################################
# Quiz
# ########################################################
class QuizQuizListAPIView(BaseListApiView):
    serializer_class = QuizSerializer
    search_fields = ['title', ]

    class QuizFilter(FilterSet):
        title = CharFilter(lookup_expr='icontains')

        class Meta:
            model = Quiz
            fields = ['id', 'title', 'publication_status', 'author']

    filterset_class = QuizFilter

    def get_queryset(self):
        queryset = Quiz.objects.all().prefetch_related('author', )
        return queryset


##########################################################
# Question Groups
# ########################################################
class QuizQuestionGroupListAPIView(BaseListApiView):
    serializer_class = QuestionGroupSerializer
    search_fields = ['title', ]

    class QuestionGroupFilter(FilterSet):
        title = CharFilter(lookup_expr='icontains')
        quiz_id = CharFilter(field_name='quiz', lookup_expr='exact')

        class Meta:
            model = QuestionGroup
            fields = ['id', 'title', 'quiz_id']

    filterset_class = QuestionGroupFilter

    def get_queryset(self):
        queryset = QuestionGroup.objects.all()
        return queryset


##########################################################
# Questions
# ########################################################

class QuizQuestionListAPIView(BaseListApiView):
    serializer_class = QuestionSerializer
    search_fields = ['title', ]

    class QuestionFilter(FilterSet):
        title = CharFilter(lookup_expr='icontains')
        group = CharFilter(field_name='group', lookup_expr='exact')
        category = CharFilter(field_name='category', lookup_expr='exact')

        class Meta:
            model = QuizQuestion
            fields = ['id', 'title', 'group', 'category']

    filterset_class = QuestionFilter

    def get_queryset(self):
        queryset = QuizQuestion.objects.all()
        return queryset


class QuizQuestionCreateAPIView(generics.CreateAPIView):
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        serializer.save()


class MCQTypeAction(BaseAction):
    name = f"{QuestionType.MULTIPLE_CHOICE.value}_action"

    @override
    def apply(self, request, instance: QuizQuestion):
        step = self.get_step_from_request(request, instance)
        if step == "main":
            serializer = QuestionSerializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return {"success": 1, "message": "Question updated successfully", "data": serializer.data}
        elif step == "options":
            serializer = MCQTypeOptionsSerializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return {"success": 1, "message": "Options updated successfully", "data": serializer.data}
        elif step == "answers":
            serializer = MultiAnswerSerializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return {"success": 1, "message": "Answers updated successfully", "data": serializer.data}
        raise BaseActionException("Invalid step")

    def get_step_from_request(self, request, instance: QuizQuestion):
        step = request.data.get('step', None)
        if step is None:
            raise BaseActionException("Step is required")
        if step not in ["main", "options", "answers"]:
            raise BaseActionException("Invalid step")
        return step


class QuizQuestionUpdateAPIView(generics.UpdateAPIView):
    available_type_actions = [
        MCQTypeAction(),
    ]

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        key = f"{instance.question_type}_action"
        for i in self.available_type_actions:
            if i.name == key:
                try:
                    response = i.apply(request, instance)
                    return Response(response, status=status.HTTP_200_OK)
                except BaseActionException as e:
                    return Response({'success': 0, 'message': str(e)}, status=e.status)
        return Response({'success': 0, "message": "`action` is invalid"}, status=status.HTTP_400_BAD_REQUEST)
