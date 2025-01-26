from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button
from django import forms
from django.shortcuts import resolve_url
from django.utils.translation import gettext_lazy as _

from apps.assignments.models import Assignment
from apps.courses.models import Course, Program
from apps.posts.models import Post
from apps.quiz.models import QuestionGroup, Question, Quiz
from .fields import ThumbnailAttachmentField


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = self.get_crisply_layout(*args, **kwargs)
        self.init_add_page_disabled(*args, **kwargs)

    def get_crisply_layout(self, *args, **kwargs):
        return self.helper.build_default_layout(self)

    def init_add_page_disabled(self, *args, **kwargs):
        pass


class PostForm(BaseForm):
    thumbnail = ThumbnailAttachmentField(help_text=_("Asynchronous save."), required=False)

    class Meta:
        model = Post
        fields = (
            "title",
            "publication_status",
            "category",
            "thumbnail",
        )

    def get_crisply_layout(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        content_editor_link_btn = Button(
            "edit-content-redirect-btn",
            _("Edit Content"),
            css_class="btn-secondary",
            onClick="window.location.href='{}'".format(
                resolve_url("my_dashboard:posts-edit-content", pk=instance.pk)) if instance else "",
            disabled=not bool(instance),
        )
        return Layout(
            Row(
                Column('title', css_class='col-md-6 mb-3'),
                Column('publication_status', css_class='col-md-6 mb-3'),
                Column('category', css_class='col-md-6 mb-3'),
                Column('thumbnail', css_class='col-md-6 mb-3'),
                Column(
                    Submit('submit', _('Save'), css_class='btn-primary'),
                    content_editor_link_btn,
                    css_class='col-md-6 mb-3'
                ),
            ),
        )

    def init_add_page_disabled(self, *args, **kwargs):
        if not kwargs['instance']:
            self.fields["thumbnail"].disabled = True


class CourseForm(BaseForm):
    thumbnail = ThumbnailAttachmentField(help_text=_("Asynchronous save."), required=False)

    class Meta:
        model = Course
        fields = (
            "title",
            "code",
            "credit",
            "duration_hours",
            "duration_weeks",
            "prerequisites",
            "keywords",
            "abbreviations",
            "objective",
            "semester",
            "category",
            "thumbnail",
        )

    def get_crisply_layout(self, *args, **kwargs):
        return Layout(
            Row(
                Column('title', css_class='col-md-6 mb-3'),
                Column(css_class='col-md-6 mb-3'),
                Column('code', css_class='col-md-6 mb-3'),
                Column('credit', css_class='col-md-6 mb-3'),
                Column('duration_hours', css_class='col-md-6 mb-3'),
                Column('duration_weeks', css_class='col-md-6 mb-3'),
                Column('prerequisites', css_class='col-md-6 mb-3'),
                Column('keywords', css_class='col-md-6 mb-3'),
                Column('abbreviations', css_class='col-md-6 mb-3'),
                Column('objective', css_class='col-md-6 mb-3'),
                Column('semester', css_class='col-md-6 mb-3'),
                Column('category', css_class='col-md-6 mb-3'),
                Column('thumbnail', css_class='col-md-6 mb-3'),
                Column(Submit('submit', _('Save'), css_class='btn btn-primary'), css_class='col-md-6 mb-3'),
            ),
        )

    def init_add_page_disabled(self, *args, **kwargs):
        if not kwargs['instance']:
            self.fields["thumbnail"].disabled = True


class ProgramForm(BaseForm):
    class Meta:
        model = Program
        fields = (
            "title",
            "slug",
            "summary",
        )

    def get_crisply_layout(self, *args, **kwargs):
        return Layout(
            Row(
                Column('title', css_class='col-md-6 mb-3'),
                Column('slug', css_class='col-md-6 mb-3'),
                Column('summary', css_class='mb-3'),
                Column(Submit('submit', _('Save'), css_class='btn btn-primary'), ),
            ),
        )


class AssignmentForm(BaseForm):
    class Meta:
        model = Assignment
        fields = (
            "title",
            "description",
            "course",
            "classroom",
            "due_date",
            "submission_requirements",
        )

    def get_crisply_layout(self, *args, **kwargs):
        return Layout(
            Row(
                Column('title', css_class='col-md-6 mb-3'),
                Column(css_class='col-md-6 mb-3'),
                Column('description', css_class='col-md-6 mb-3'),
                Column('submission_requirements', css_class='col-md-6 mb-3'),
                Column('course', css_class='col-md-6 mb-3'),
                Column('classroom', css_class='col-md-6 mb-3'),
                Column(Submit('submit', _('Save'), css_class='btn btn-primary'), ),
            ),
        )


class QuizForm(BaseForm):
    class Meta:
        model = Quiz
        fields = ['title', ]

    def get_crisply_layout(self, *args, **kwargs):
        return Layout(
            Row(
                Column('title', css_class='col-md-6 mb-3'),
                Column(Submit('submit', _('Save'), css_class='btn btn-primary'), ),
            ),
        )


class QuestionGroupForm(BaseForm):
    class Meta:
        model = QuestionGroup
        fields = ['title', 'parent']

    def get_crisply_layout(self, *args, **kwargs):
        return Layout(
            Row(
                Column('title', css_class='col-md-6 mb-3'),
                Column('parent', css_class='col-md-6 mb-3'),
                Column(Submit('submit', _('Save'), css_class='btn btn-primary'), ),
            ),
        )


class QuestionForm(BaseForm):
    class Meta:
        model = Question
        fields = ['title', 'text']

    def get_crisply_layout(self, *args, **kwargs):
        return Layout(
            Row(
                Column('title', css_class='col-md-6 mb-3'),
                Column('text', css_class='col-md-6 mb-3'),
                Column(Submit('submit', _('Save'), css_class='btn btn-primary'), ),
            ),
        )
