from django.contrib import messages
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import resolve_url, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from apps.dashboard.quiz.forms import QuizForm, QuestionForm, QuestionGroupForm, MultipleChoiceFormSet
from apps.quizzes.models import Quiz, QuizQuestion, QuestionGroup, QuestionType
from lms.crud_base.tables import Table, Column, ActionsColumn, DefaultDeleteAction, DefaultEditAction, ButtonAction
from lms.crud_base.views import BaseCreateView, BaseUpdateView, get_default_add_success_message, \
    get_default_update_success_message, BaseListView
from .url_reverses import url_reverses_dict


########################################################################################################################
# Quiz
########################################################################################################################

class QuizQuizListView(BaseListView):
    model = Quiz
    page_list_url = reverse_lazy("dashboard:quiz-quiz-list")
    template_name = "lms/dashboard/quiz/quiz_list.html"

    class QuizTable(Table):
        id = Column(field_name="id", header="#", orderable=True)
        title = Column(field_name="title")
        actions = ActionsColumn(
            actions=[
                DefaultEditAction(
                    redirect_url_name=url_reverses_dict["quiz-quiz-update"],
                ),
                DefaultDeleteAction(
                    redirect_url_name=url_reverses_dict["quiz-quiz-update"],
                ),
            ],
            extra_actions=[
                ButtonAction(
                    name="open-question-groups",
                    redirect_url_name=reverse_lazy("dashboard:quiz-question-group-list"),
                    label=_("Questions Groups"),
                )
            ],
        )

        class Meta:
            model = QuizQuestion
            source_url = reverse_lazy("dashboard:quiz-quiz-list-api")
            fields = ['id', 'title', 'actions']

    table = QuizTable()

    def get_urls(self):
        return {
            'add': resolve_url('dashboard:quiz-quiz-create'),
        }


class QuizQuizCreateView(BaseCreateView):
    model = Quiz
    form_class = QuizForm
    page_list_url = reverse_lazy("dashboard:quiz-quiz-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_message(self, obj):
        return get_default_add_success_message(obj.title, obj.id)

    def get_success_url(self):
        return resolve_url("dashboard:quiz-quiz-update", pk=self.object.pk)


class QuizQuizUpdateView(BaseUpdateView):
    model = Quiz
    form_class = QuizForm
    page_list_url = reverse_lazy("dashboard:quiz-quiz-list")

    def get_success_message(self, obj):
        return get_default_update_success_message(obj.title, obj.id)

    def get_success_url(self):
        return resolve_url("dashboard:quiz-quiz-update", pk=self.object.pk)


class QuizQuizDeleteView(generic.DeleteView):
    template_name = "lms/dashboard/quiz/quiz_delete.html"
    model = Quiz

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        msg = _("Deleted post '%s'") % self.object.title
        messages.success(self.request, msg)
        return reverse("dashboard:quiz-quiz-list")


class UseQuizNestedMixin:
    quiz_obj = None

    def render_select_question_quiz_view(self):
        self.template_name = "lms/dashboard/quiz/question_select_quiz.html"
        return self.render_to_response({
            "urls": {
                "quizListApi": reverse("dashboard:quiz-quiz-list-api"),
            }
        })

    def get_quiz_object(self):
        return Quiz.objects.get(pk=self.kwargs.get("quiz_id"))

    def get(self, request, *args, **kwargs):
        quiz_id = request.GET.get("quiz_id", None)
        if quiz_id is None:
            return self.render_select_question_quiz_view()

        self.quiz_obj = get_object_or_404(Quiz, pk=quiz_id)

        if not self.quiz_obj:
            return self.http_method_not_allowed(request, *args, **kwargs)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        quiz_id = request.POST.get("quiz_id", None)
        if quiz_id is None:
            quiz_id = request.GET.get("quiz_id", None)
        if quiz_id is None:
            return HttpResponseBadRequest("quiz_id is required")

        self.quiz_obj = get_object_or_404(Quiz, pk=quiz_id)

        if not self.quiz_obj:
            return self.http_method_not_allowed(request, *args, **kwargs)

        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "quiz": self.quiz_obj,
        })
        return context

    def get_breadcrumbs(self, context):
        default = super().get_breadcrumbs(context)
        default[1]["url"] = self.page_list_url + f"?quiz_id={self.quiz_obj.id}"
        return default


class UseQuizAndGroupNestedMixin:
    group_obj = None

    def render_select_question_group_view(self):
        self.template_name = "lms/dashboard/quiz/question_select_group.html"
        return self.render_to_response({
            "urls": {
                "groupListApi": reverse("dashboard:quiz-question-group-list-api"),
            }
        })

    def get_group_object(self):
        return QuestionGroup.objects.get(pk=self.kwargs.get("group_id"))

    def get(self, request, *args, **kwargs):
        group_id = request.GET.get("question_group_id", None)
        if group_id is None:
            return self.render_select_question_group_view()

        self.group_obj = get_object_or_404(QuestionGroup, pk=group_id)

        if not self.group_obj:
            return self.http_method_not_allowed(request, *args, **kwargs)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        group_id = request.POST.get("question_group_id", None)
        if group_id is None:
            group_id = request.GET.get("question_group_id", None)
        if group_id is None:
            return HttpResponseBadRequest("group_id is required")

        self.group_obj = get_object_or_404(Quiz, pk=group_id)

        if not self.group_obj:
            return self.http_method_not_allowed(request, *args, **kwargs)

        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "question_group": self.group_obj,
        })
        return context

    def get_breadcrumbs(self, context):
        default = super().get_breadcrumbs(context)
        default[1]["url"] = self.page_list_url + f"?question_group_id={self.group_obj.id}"
        return default


########################################################################################################################
# Question Group
########################################################################################################################

class QuizQuestionGroupListView(UseQuizNestedMixin, BaseListView):
    model = QuestionGroup
    page_list_url = reverse_lazy("dashboard:quiz-question-group-list")
    template_name = "lms/dashboard/quiz/question_group_list.html"

    class QGroupTable(Table):
        id = Column(field_name="id", header="#", orderable=True)
        title = Column(field_name="title")
        actions = ActionsColumn(
            actions=[
                DefaultEditAction(
                    redirect_url_name=url_reverses_dict["quiz-question-group-update"]
                ),
                DefaultDeleteAction(
                    redirect_url_name=url_reverses_dict["quiz-question-group-delete"]
                ),
            ],
            extra_actions=[
                ButtonAction(
                    name="open-questions",
                    redirect_url_name=reverse_lazy("dashboard:quiz-question-list"),
                    label=_("Questions"),
                )
            ],
        )

        class Meta:
            model = QuestionGroup
            source_url = reverse_lazy("dashboard:quiz-question-group-list-api")
            fields = ['id', 'title', 'actions']

    table = QGroupTable()

    def get_urls(self):
        return {
            'add': resolve_url('dashboard:quiz-question-group-create'),
        }


class QuizQuestionGroupCreateView(UseQuizNestedMixin, BaseCreateView):
    model = QuestionGroup
    form_class = QuestionGroupForm
    page_list_url = reverse_lazy("dashboard:quiz-question-group-list")

    def form_valid(self, form):
        form.instance.quiz = self.quiz_obj
        print("create group", form.instance.quiz, self.quiz_obj)
        return super().form_valid(form)

    def get_success_message(self, obj):
        return get_default_add_success_message(obj.title, obj.id)

    def get_success_url(self):
        return resolve_url("dashboard:quiz-question-group-update",
                           pk=self.object.pk) + f"?quiz_id={self.object.quiz_id}"


class QuizQuestionGroupUpdateView(UseQuizNestedMixin, BaseUpdateView):
    model = QuestionGroup
    form_class = QuestionGroupForm
    page_list_url = reverse_lazy("dashboard:quiz-question-group-list")

    def get_success_message(self, obj):
        return get_default_update_success_message(obj.title, obj.id)

    def get_success_url(self):
        return resolve_url("dashboard:quiz-question-group-update",
                           pk=self.object.pk) + f"?quiz_id={self.object.quiz_id}"


########################################################################################################################
# Question
########################################################################################################################

class QuizQuestionListView(UseQuizAndGroupNestedMixin, BaseListView):
    model = QuizQuestion
    page_list_url = reverse_lazy("dashboard:quiz-question-list")
    template_name = "lms/dashboard/quiz/question_list.html"

    class QuestionTable(Table):
        id = Column(field_name="id", header="#", orderable=True)
        title = Column(field_name="title")
        question_type = Column(field_name="question_type")
        actions = ActionsColumn(
            actions=[
                DefaultEditAction(
                    redirect_url_name=url_reverses_dict["quiz-question-update"],
                ),
                DefaultDeleteAction(
                    redirect_url_name=url_reverses_dict["quiz-question-update"],
                ),
            ],
        )

        class Meta:
            model = QuizQuestion
            source_url = reverse_lazy('dashboard:quiz-question-list-api')
            fields = ['id', 'title', 'question_type', 'actions']

    table = QuestionTable()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = self.group_obj.quiz
        question_groups = QuestionGroup.objects.filter(quiz=quiz, parent=None)
        context.update({
            "bank": {
                "navigation": {
                    "groups": question_groups,
                }
            },
            "group": self.group_obj,
            "form": QuestionForm(),
        })
        return context

    def get_urls(self):
        return {}


class QuizQuestionFormView(generic.View):
    def get(self, request, *args, **kwargs):
        question_type = request.GET.get("question_type", None)
        question_id = request.GET.get("question_id", None)

        if question_type is None:
            return HttpResponseBadRequest("question_type is required")
        if question_id is None:
            return HttpResponseBadRequest("question_id is required")

        try:
            question_obj = QuizQuestion.objects.get(pk=question_id)
        except QuizQuestion.DoesNotExist:
            return HttpResponseBadRequest("Question does not exist")
        if question_type == QuestionType.MULTIPLE_CHOICE:
            form_html = render_to_string("lms/dashboard/partials/quiz/multiple_choice_form.html", {
                "formset": MultipleChoiceFormSet()
            })
        else:
            form_html = "Incorrect question type"

        return JsonResponse({"form_html": form_html})


class QuizQuestionUpdateView(UseQuizAndGroupNestedMixin, BaseUpdateView):
    model = QuizQuestion
    form_class = QuestionForm
    page_list_url = reverse_lazy("dashboard:quiz-question-list")
    template_name = "lms/dashboard/quiz/question_form.html"

    def get_success_message(self, obj):
        return get_default_update_success_message(obj.title, obj.id)

    def get_success_url(self):
        return resolve_url("dashboard:quiz-question-update", pk=self.object.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.object
        print("instance", instance)
        if instance.question_type == QuestionType.MULTIPLE_CHOICE:
            context.update({
                "answers_formset": MultipleChoiceFormSet(),
            })
        return context

    def get_template_names(self):
        super().get_template_names()
        return ["lms/dashboard/quiz/question_form.html"]
