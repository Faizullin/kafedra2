# pylint: disable=W0201

from django.apps import apps
from django.conf import settings
from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView

from .core.application import LmsConfig
from .core.loading import get_class


class LmsPortal(LmsConfig):
    name = "lms"

    def ready(self):
        from django.contrib.auth.forms import SetPasswordForm

        self.accounts_app = apps.get_app_config("accounts")
        self.pages_app = apps.get_app_config("pages")
        # self.catalogue_app = apps.get_app_config("catalogue")
        # self.customer_app = apps.get_app_config("customer")
        # self.basket_app = apps.get_app_config("basket")
        # self.checkout_app = apps.get_app_config("checkout")
        # self.search_app = apps.get_app_config("search")
        self.dashboard_app = apps.get_app_config("dashboard")
        # self.offer_app = apps.get_app_config("offer")
        # self.wishlists_app = apps.get_app_config("wishlists")

        self.password_reset_form = get_class("accounts.forms", "PasswordResetForm")
        self.set_password_form = SetPasswordForm

    def get_urls(self):
        from django.contrib.auth import views as auth_views

        from .views.decorators import login_forbidden

        urls = [
            path("", self.pages_app.urls),
            # path("catalogue/", self.catalogue_app.urls),
            # path("basket/", self.basket_app.urls),
            # path("checkout/", self.checkout_app.urls),
            # path("accounts/", self.accounts_app.urls),
            path("", self.accounts_app.urls),
            # path("search/", self.search_app.urls),
            path("", self.dashboard_app.urls),
            # path("offers/", self.offer_app.urls),
            # path("wishlists/", self.wishlists_app.urls),
            # Password reset - as we're using Django's default view functions,
            # we can't namespace these urls as that prevents
            # the reverse function from working.
            path(
                "password-reset/",
                login_forbidden(
                    auth_views.PasswordResetView.as_view(
                        form_class=self.password_reset_form,
                        success_url=reverse_lazy("password-reset-done"),
                        template_name="lms/registration/password_reset_form.html",
                    )
                ),
                name="password-reset",
            ),
            path(
                "password-reset/done/",
                login_forbidden(
                    auth_views.PasswordResetDoneView.as_view(
                        template_name="lms/registration/password_reset_done.html"
                    )
                ),
                name="password-reset-done",
            ),
            path(
                "password-reset/confirm/<str:uidb64>/<str:token>/",
                login_forbidden(
                    auth_views.PasswordResetConfirmView.as_view(
                        form_class=self.set_password_form,
                        success_url=reverse_lazy("password-reset-complete"),
                        template_name="lms/registration/password_reset_confirm.html",
                    )
                ),
                name="password-reset-confirm",
            ),
            path(
                "password-reset/complete/",
                login_forbidden(
                    auth_views.PasswordResetCompleteView.as_view(
                        template_name="lms/registration/password_reset_complete.html"
                    )
                ),
                name="password-reset-complete",
            ),
        ]
        return urls
