from django.utils.translation import gettext_lazy as _

from lms.core.application import LmsDashboardConfig
from lms.core.loading import get_class


class QuizDashboardConfig(LmsDashboardConfig):
    label = "quiz_dashboard"
    name = "apps.dashboard.quiz"
    verbose_name = _("Quiz")

    default_permissions = [
        "is_staff",
    ]

    def configure_permissions(self):
        DashboardPermission = get_class("dashboard.permissions", "DashboardPermission")

        self.permissions_map = {
            "quiz-post": (
                DashboardPermission.get("quiz"),
            ),
            "quiz-create": (
                DashboardPermission.get("quiz"),
            ),
            "quiz-list": (
                DashboardPermission.get("quiz"),
            ),
            "quiz-delete": (
                DashboardPermission.get("quiz"),
            ),
        }

    def ready(self):
        from apps.dashboard.quiz.views import QuizQuizListView, QuizQuizCreateView, QuizQuestionListView, \
            QuizQuestionUpdateView, QuizQuizUpdateView, QuizQuestionGroupListView, \
            QuizQuestionGroupCreateView, QuizQuestionGroupUpdateView, QuizQuestionFormView
        from apps.dashboard.quiz.api.views import QuizQuestionGroupListAPIView, QuizQuizListAPIView, \
            QuizQuestionListAPIView, QuizQuestionCreateAPIView, QuizQuestionUpdateAPIView

        self.quiz_quiz_list_view = QuizQuizListView
        self.quiz_quiz_list_api_view = QuizQuizListAPIView
        self.quiz_quiz_create_view = QuizQuizCreateView
        self.quiz_quiz_update_view = QuizQuizUpdateView

        self.quiz_question_group_list_view = QuizQuestionGroupListView
        self.quiz_question_group_list_api_view = QuizQuestionGroupListAPIView
        self.quiz_question_group_create_view = QuizQuestionGroupCreateView
        self.quiz_question_group_update_view = QuizQuestionGroupUpdateView

        self.quiz_question_list_view = QuizQuestionListView
        self.quiz_question_list_api_view = QuizQuestionListAPIView
        self.quiz_question_update_view = QuizQuestionUpdateView
        self.quiz_question_qtype_detail_view = QuizQuestionFormView

        self.quiz_question_create_api_view = QuizQuestionCreateAPIView
        self.quiz_question_update_api_view = QuizQuestionUpdateAPIView

        super().ready()

    def get_urls(self):
        urls = [
            self.get_path_with_reverses(self.quiz_quiz_list_view.as_view(), "quiz-quiz-list"),
            self.get_path_with_reverses(self.quiz_quiz_list_api_view.as_view(), "quiz-quiz-list-api"),
            self.get_path_with_reverses(self.quiz_quiz_create_view.as_view(), "quiz-quiz-create", ),
            self.get_path_with_reverses(self.quiz_quiz_update_view.as_view(), "quiz-quiz-update", ),
            self.get_path_with_reverses(
                self.quiz_question_group_list_view.as_view(),
                "quiz-question-group-list",
            ),
            self.get_path_with_reverses(
                self.quiz_question_group_list_api_view.as_view(),
                "quiz-question-group-list-api",
            ),
            self.get_path_with_reverses(
                self.quiz_question_group_create_view.as_view(),
                'quiz-question-group-create'
            ),
            self.get_path_with_reverses(
                self.quiz_question_group_update_view.as_view(),
                'quiz-question-group-update'
            ),
            self.get_path_with_reverses(
                self.quiz_question_list_view.as_view(),
                'quiz-question-list'
            ),
            self.get_path_with_reverses(
                self.quiz_question_list_api_view.as_view(),
                'quiz-question-list-api'
            ),
            self.get_path_with_reverses(
                self.quiz_question_update_view.as_view(),
                'quiz-question-update'
            ),
            self.get_path_with_reverses(
                self.quiz_question_qtype_detail_view.as_view(),
                'quiz-question-qtype-detail'
            ),
            self.get_path_with_reverses(
                self.quiz_question_create_api_view.as_view(),
                'quiz-question-create-api'
            ),
            self.get_path_with_reverses(
                self.quiz_question_update_api_view.as_view(),
                'quiz-question-update-api'
            ),
        ]

        return self.post_process_urls(urls)
