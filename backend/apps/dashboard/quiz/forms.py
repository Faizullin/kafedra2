from crispy_forms.layout import Layout, Row, Column, Submit, Button
from django.forms import inlineformset_factory
from django.shortcuts import resolve_url
from django.utils.translation import gettext as _

from apps.quizzes.models import Quiz, QuizQuestion, QuestionGroup, QuestionAnswer, MultipleChoiceOptions
from lms.crud_base.forms import BaseForm, forms


class QuizForm(BaseForm):
    class Meta:
        model = Quiz
        fields = (
            "title",
            "publication_status",
        )

    def get_crisply_layout(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        question_list_link_btn = Button(
            "edit-content-redirect-btn",
            _("Question Groups"),
            css_class="btn-secondary",
            onClick="window.location.href='{}'".format(
                resolve_url("dashboard:quiz-question-group-list") + f"?quiz_id={instance.pk}") if instance else "",
            disabled=not bool(instance),
        )
        return Layout(
            Row(
                Column('title', css_class='col-md-6 mb-3'),
                Column('publication_status', css_class='col-md-6 mb-3'),
                Column(
                    Submit('submit', _('Save'), css_class='btn-primary'),
                    question_list_link_btn,
                    css_class='col-md-6 mb-3'
                ),
            ),
        )


class QuestionGroupForm(BaseForm):
    class Meta:
        model = QuestionGroup
        fields = (
            "title",
        )

    def get_crisply_layout(self, *args, **kwargs):
        instance = kwargs.get('instance', None)

        return Layout(
            Row(
                Column('title', css_class='col-md-6 mb-3'),
                Column(
                    Submit('submit', _('Save'), css_class='btn-primary'),
                    css_class='col-md-6 mb-3'
                ),
            ),
        )


class QuestionForm(BaseForm):
    class Meta:
        model = QuizQuestion
        fields = (
            "title",
            "text",
            "group",
            "category",
            "question_type",
        )

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['group'].required = True
        self.fields['question_type'].required = True

    def get_crisply_layout(self, *args, **kwargs):
        instance = kwargs.get('instance', None)

        return Layout(
            Row(
                Column('title', css_class='col-md-6 mb-3'),
                Column('text', css_class='col-md-6 mb-3'),
                Column('group', css_class='col-md-6 mb-3'),
                Column('category', css_class='col-md-6 mb-3'),
                Column('question_type', css_class='col-md-6 mb-3'),
                Column(
                    Submit('submit', _('Save'), css_class='btn-primary'),
                    css_class='col-md-6 mb-3'
                ) if not instance else "",
            ),
        )


class MultipleChoiceAnswerForm(BaseForm):
    answer = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    feedback = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = QuestionAnswer
        fields = (
            "answer",
            "fraction",
            "feedback",
        )

    def get_crisply_layout(self, *args, **kwargs):
        instance = kwargs.get('instance', None)

        return Layout(
            Row(
                Column('answer', css_class='col-md-6 mb-3 answer-answer-text-field-container'),
                Column('fraction', css_class='col-md-6 mb-3 answer-fraction-field-container'),
                Column('feedback', css_class='col-md-6 mb-3'),
            ),
        )


class MultipleChoiceOptionsForm(BaseForm):
    class Meta:
        model = MultipleChoiceOptions
        fields = (
            "single",
            "shuffle_answers",
            "correct_feedback",
            "partially_correct_feedback",
            "incorrect_feedback",
            "answer_numbering",
            "show_num_correct",
        )

    def get_crisply_layout(self, *args, **kwargs):
        instance = kwargs.get('instance', None)

        return Layout(
            Row(
                Column('single', css_class='col-md-6 mb-3'),
                Column('shuffle_answers', css_class='col-md-6 mb-3'),
                Column('correct_feedback', css_class='col-md-6 mb-3'),
                Column('partially_correct_feedback', css_class='col-md-6 mb-3'),
                Column('incorrect_feedback', css_class='col-md-6 mb-3'),
                Column('answer_numbering', css_class='col-md-6 mb-3'),
                Column('show_num_correct', css_class='col-md-6 mb-3'),
                Column(
                    Submit('submit', _('Save'), css_class='btn-primary'),
                    css_class='col-md-6 mb-3'
                ) if not instance else "",
            ),
        )


MultipleChoiceFormSet = inlineformset_factory(
    QuizQuestion, QuestionAnswer,
    form=MultipleChoiceAnswerForm,
    extra=2,
    can_delete=True
)
