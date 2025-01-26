from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import resolve_url
from django.utils.translation import gettext as _
from django.views.generic import CreateView, UpdateView


def get_default_add_success_message(name, id):
    return "\"{}\"[{}] has been created".format(name, id)

def get_default_update_success_message(name, id):
    return "\"{}\"[{}] has been updated".format(name, id)

class BaseBreadcrumbsViewMixin(object):
    def get_breadcrumbs(self, context):
        return [
            {"label": _("Dashboard"), "url": resolve_url("dashboard:index")},
            {"label": self.page_model_name_plural, "url": self.page_list_url},
            {"label": context['title'], "current": True},
        ]

class UseContextUrlsMixin(object):
    def get_urls(self):
        raise []


class BaseCreateView(BaseBreadcrumbsViewMixin, UseContextUrlsMixin, CreateView):
    template_name = "lms/dashboard/pages/items/items-edit.html"
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
        })
        context["breadcrumbs"] = self.get_breadcrumbs(context)
        context["urls"] = self.get_urls()
        return context

    def get_success_message(self, obj):
        raise Exception("Not implemented")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.get_success_message(form.instance))
        return response


class BaseUpdateView(BaseBreadcrumbsViewMixin, UseContextUrlsMixin, UpdateView):
    template_name = "lms/dashboard/pages/items/items-edit.html"
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
            'instance': instance,
            'attachments': {
                "content_type": ContentType.objects.get_for_model(instance).model,
                "object_id": instance.pk
            }
        })
        context["breadcrumbs"] = self.get_breadcrumbs(context)
        context["urls"] = self.get_urls()
        return context

    def get_success_message(self, obj):
        raise Exception("Not implemented")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.get_success_message(form.instance))
        return response


__ALL__ = [ "BaseCreateView", "BaseUpdateView" ,]