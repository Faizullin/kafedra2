from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, resolve_url
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView, TemplateView, DetailView

from apps.accounts.models import Student
from apps.activities.models import ActivityLog
from apps.courses.models import Course, Program
from apps.posts.models import Post
from .forms import PostForm, CourseForm, ProgramForm, AssignmentForm
from ..assignments.models import Assignment

UserModel = get_user_model()


@login_required
def dashboard_home_view(request):
    context = {
        # "items": items,
    }
    return render(request, "dashboard/pages/home.html", context)


def get_default_add_success_message(name, id):
    return "\"{}\"[{}] has been created".format(name, id)


def get_default_update_success_message(name, id):
    return "\"{}\"[{}] has been updated".format(name, id)


class BaseListView(LoginRequiredMixin, TemplateView):
    page_model = None
    page_list_url: str = None
    page_create_url: str = None
    page_update_url: str = None
    page_list_api_url: str = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_model_name = self.page_model._meta.verbose_name
        self.page_model_name_plural = self.page_model._meta.verbose_name_plural

    def get_context_data(self, *args, **kwargs):
        name = self.page_model_name
        name_plural = self.page_model_name_plural
        context = {
            'title': name_plural,
            'page_header_title': name_plural,
            'card_header_title': _("List"),
            'breadcrumbs': [
                {"label": _("Dashboard"), "url": resolve_url("my_dashboard:home")},
                {"label": name_plural, "url": self.page_list_url},
                {"label": _("List"), "current": True},
            ],
            "urls": {
                "list-api": self.page_list_api_url,
                "create": self.page_create_url,
                "update": self.page_update_url,
            },
        }
        return context


class BaseCreateView(LoginRequiredMixin, CreateView):
    template_name = "dashboard/pages/items/items-edit.html"
    page_list_url: str = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_model_name = self.model._meta.verbose_name
        self.page_model_name_plural = self.model._meta.verbose_name_plural

    def get_initial_super_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_context_data(self, **kwargs):
        context = self.get_initial_super_context_data(**kwargs)
        title = _("Add") + " " + self.page_model_name
        context.update({
            'title': title,
            'page_header_title': title,
            'card_header_title': _("New") + " " + self.page_model_name,
            'breadcrumbs': [
                {"label": _("Dashboard"), "url": resolve_url("my_dashboard:home")},
                {"label": self.page_model_name_plural, "url": self.page_list_url},
                {"label": title, "current": True},
            ],
        })
        return context

    def get_success_message(self, obj):
        raise Exception("Not implemented")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.get_success_message(form.instance))
        return response


class BaseUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "dashboard/pages/items/items-edit.html"
    page_list_url: str = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_model_name = self.model._meta.verbose_name
        self.page_model_name_plural = self.model._meta.verbose_name_plural

    def get_initial_super_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_context_data(self, **kwargs):
        context = self.get_initial_super_context_data(**kwargs)
        instance = self.object
        title = "{} {} [{}]".format(_("Edit"), self.page_model_name, str(instance.pk))
        context.update({
            'title': title,
            'page_header_title': title,
            'card_header_title': "{} [{}]".format(instance.title, instance.pk),
            'breadcrumbs': [
                {"label": _("Dashboard"), "url": resolve_url("my_dashboard:home")},
                {"label": self.page_model_name_plural, "url": self.page_list_url},
                {"label": title, "current": True},
            ],
            'instance': instance,
            'attachments': {
                "content_type": ContentType.objects.get_for_model(instance).model,
                "object_id": instance.pk
            }
        })
        return context

    def get_success_message(self, obj):
        raise Exception("Not implemented")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.get_success_message(form.instance))
        return response


##########################################################
# Posts
# ########################################################
class PostListView(BaseListView):
    template_name = "dashboard/pages/posts/posts_list.html"
    page_model = Post
    page_list_url = reverse_lazy("resources-posts-list")
    page_create_url = reverse_lazy("my_dashboard:posts-add")
    page_update_url = reverse_lazy("my_dashboard:posts-edit", pk=0)
    page_list_api_url = reverse_lazy("my_dashboard-api:posts-list-api")
    # permission_required = ('posts.change_pallet')


class PostCreateView(BaseCreateView):
    model = Post
    form_class = PostForm
    page_list_url = reverse_lazy("resources-posts-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_type = "posts"
        return super().form_valid(form)

    def get_success_message(self, obj):
        return get_default_add_success_message(obj.title, obj.id)

    def get_success_url(self):
        return resolve_url("my_dashboard:posts-edit", pk=self.object.pk)


class PostUpdateView(BaseUpdateView):
    model = Post
    form_class = PostForm
    page_list_url = reverse_lazy("resources-posts-list")

    def get_success_message(self, obj):
        return get_default_update_success_message(obj.title, obj.id)

    def get_success_url(self):
        return resolve_url("my_dashboard:posts-edit", pk=self.object.pk)


class PostEditContentView(DetailView):
    template_name = "dashboard/pages/posts/posts_edit_content.html"

    def get_context_data(self, **kwargs):
        context = self.get_context_data(**kwargs)

        js_src_list = [
            "https://cdn.jsdelivr.net/npm/@editorjs/editorjs@latest",
        ]
        PLUGINS = (
            '@editorjs/paragraph',
            '@editorjs/image',
            '@editorjs/header',
            '@editorjs/list',
            '@editorjs/checklist',
            '@editorjs/quote',
            '@editorjs/raw',
            '@editorjs/code',
            '@editorjs/inline-code',
            '@editorjs/embed',
            '@editorjs/delimiter',
            '@editorjs/warning',
            '@editorjs/link',
            '@editorjs/marker',
            '@editorjs/table',
        )
        for i in PLUGINS:
            js_src_list.append("https://cdn.jsdelivr.net/npm/{}@latest".format(i))

        instance = context["object"]
        title = "{} {} [{}]".format(_("Edit"), _("Post"), str(instance.pk))
        context.update({
            'title': title,
            'page_header_title': title,
            'card_header_title': "{} [{}]".format(instance.title, instance.pk),
            'breadcrumbs': [
                {"label": _("Dashboard"), "url": resolve_url("my_dashboard:home")},
                {"label": _("Posts"), "url": resolve_url("my_dashboard:posts-list")},
                {"label": title, "url": resolve_url("my_dashboard:posts-edit", pk=instance.pk)},
                {"label": _("Edit Content"), "current": True},
            ],
            "editor": {
                "media": {
                    "js": js_src_list,
                    "css": (),
                },
            },
            "instance": instance,
            "attachments": {
                "content_type": ContentType.objects.get_for_model(instance).model,
                "object_id": instance.pk,
            },
        })
        return context


##########################################################
# Courses
# ########################################################
class CourseListView(BaseListView):
    template_name = "dashboard/pages/courses/courses_list.html"
    page_model = Course
    page_list_url = reverse_lazy("my_dashboard:courses-list")
    page_create_url = reverse_lazy("my_dashboard:courses-add")
    page_update_url = reverse_lazy("my_dashboard:courses-edit", pk=0)
    page_list_api_url = reverse_lazy("my_dashboard-api:courses-list-api")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            "courses": Course.objects.all().select_related("thumbnail", "category"),
        })
        return context


class CourseCreateView(BaseCreateView):
    model = Course
    form_class = CourseForm
    page_list_url = reverse_lazy("my_dashboard:courses-list")

    def get_success_message(self, obj):
        return get_default_add_success_message(obj.title, obj.id)

    def get_success_url(self):
        return resolve_url("my_dashboard:courses-edit", pk=self.object.pk)


class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    page_list_url = reverse_lazy("my_dashboard:courses-list")

    def get_success_message(self, obj):
        return get_default_update_success_message(obj.title, obj.id)

    def get_success_url(self):
        return resolve_url("my_dashboard:courses-edit", pk=self.object.pk)


##########################################################
# Programs
# ########################################################
class ProgramListView(BaseListView):
    template_name = "dashboard/pages/programs/programs_list.html"
    page_model = Program
    page_list_url = reverse_lazy("my_dashboard:programs-list")
    page_create_url = reverse_lazy("my_dashboard:programs-add")
    page_update_url = reverse_lazy("my_dashboard:programs-edit", pk=0)
    page_list_api_url = reverse_lazy("my_dashboard-api:programs-list-api")


class ProgramCreateView(BaseCreateView):
    model = Program
    form_class = ProgramForm
    page_list_url = reverse_lazy("my_dashboard:programs-list")

    def get_success_message(self, obj):
        return get_default_update_success_message(obj.title, obj.id)

    def get_success_url(self):
        return resolve_url("my_dashboard:programs-edit", pk=self.object.pk)


class ProgramUpdateView(UpdateView):
    model = Program
    form_class = ProgramForm

    def get_success_message(self, obj):
        return get_default_update_success_message(obj.title, obj.id)

    def get_success_url(self):
        return resolve_url("my_dashboard:programs-edit", pk=self.object.pk)


##########################################################
# Students
# ########################################################
class StudentListView(BaseListView):
    template_name = "dashboard/pages/students/students_list.html"
    page_model = Student
    page_list_url = reverse_lazy("my_dashboard:students-list")
    page_create_url = reverse_lazy("my_dashboard:students-add")
    page_update_url = reverse_lazy("my_dashboard:students-edit", pk=0)
    page_list_api_url = reverse_lazy("my_dashboard-api:students-list-api")


##########################################################
# ActivityLogs
# ########################################################
class ActivityLogListView(BaseListView):
    page_model = ActivityLog
    page_list_url = reverse_lazy("my_dashboard:activity_logs-list")
    page_list_api_url = reverse_lazy("my_dashboard-api:activity_logs-list-api")


##########################################################
# Assignment
# ########################################################
class AssignmentListView(BaseListView):
    page_model = Assignment
    page_list_url = reverse_lazy("my_dashboard:assignments-list")
    page_create_url = reverse_lazy("my_dashboard:assignments-add")
    page_update_url = reverse_lazy("my_dashboard:assignments-edit", pk=0)
    page_list_api_url = reverse_lazy("my_dashboard-api:assignments-list-api")


class AssignmentCreateView(BaseCreateView):
    model = Assignment
    form_class = AssignmentForm
    page_list_url = reverse_lazy("my_dashboard:assignments-list")

    def get_success_message(self, obj):
        return get_default_add_success_message(obj.title, obj.id)

    def get_success_url(self):
        return resolve_url("my_dashboard:assignments-edit", pk=self.object.pk)


class AssignmentUpdateView(UpdateView):
    model = Assignment
    form_class = AssignmentForm
    page_list_url = reverse_lazy("my_dashboard:assignments-list")

    def get_success_message(self, obj):
        return get_default_update_success_message(obj.title, obj.id)

    def get_success_url(self):
        return resolve_url("my_dashboard:assignments-edit", pk=self.object.pk)


# ########################################################
# News & Events Home
# ########################################################
@login_required
def home_view(request):
    items = Post.objects.filter(post_type="news_and_posts").all().order_by("-created_at")
    context = {
        "title": _("News & Events"),
        "items": items,
    }
    return render(request, "dashboard/pages/home.html", context)
