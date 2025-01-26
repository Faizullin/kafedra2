# Use 'alpha', 'beta', 'rc' or 'final' as the 4th element to indicate release type.
VERSION = (4, 0, 0, "alpha", 1)


def get_short_version():
    return "%s.%s" % (VERSION[0], VERSION[1])


def get_version():
    version = "%s.%s" % (VERSION[0], VERSION[1])
    # Append 3rd digit if > 0
    if VERSION[2]:
        version = "%s.%s" % (version, VERSION[2])

    if len(VERSION) > 3 and VERSION[3] != "final":
        mapping = {"alpha": "a", "beta": "b", "rc": "rc"}
        version = "%s%s" % (version, mapping[VERSION[3]])
        if len(VERSION) == 5:
            version = "%s%s" % (version, VERSION[4])

    return version


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.flatpages",
    "lms.config.Shop",
    "lms.apps.analytics.apps.AnalyticsConfig",
    "lms.apps.checkout.apps.CheckoutConfig",
    "lms.apps.address.apps.AddressConfig",
    "lms.apps.shipping.apps.ShippingConfig",
    "lms.apps.catalogue.apps.CatalogueConfig",
    "lms.apps.catalogue.reviews.apps.CatalogueReviewsConfig",
    "lms.apps.communication.apps.CommunicationConfig",
    "lms.apps.partner.apps.PartnerConfig",
    "lms.apps.basket.apps.BasketConfig",
    "lms.apps.payment.apps.PaymentConfig",
    "lms.apps.offer.apps.OfferConfig",
    "lms.apps.order.apps.OrderConfig",
    "lms.apps.customer.apps.CustomerConfig",
    "lms.apps.search.apps.SearchConfig",
    "lms.apps.voucher.apps.VoucherConfig",
    "lms.apps.wishlists.apps.WishlistsConfig",
    "lms.apps.dashboard.apps.DashboardConfig",
    "lms.apps.dashboard.reports.apps.ReportsDashboardConfig",
    "lms.apps.dashboard.users.apps.UsersDashboardConfig",
    "lms.apps.dashboard.orders.apps.OrdersDashboardConfig",
    "lms.apps.dashboard.catalogue.apps.CatalogueDashboardConfig",
    "lms.apps.dashboard.offers.apps.OffersDashboardConfig",
    "lms.apps.dashboard.partners.apps.PartnersDashboardConfig",
    "lms.apps.dashboard.pages.apps.PagesDashboardConfig",
    "lms.apps.dashboard.ranges.apps.RangesDashboardConfig",
    "lms.apps.dashboard.reviews.apps.ReviewsDashboardConfig",
    "lms.apps.dashboard.vouchers.apps.VouchersDashboardConfig",
    "lms.apps.dashboard.communications.apps.CommunicationsDashboardConfig",
    "lms.apps.dashboard.shipping.apps.ShippingDashboardConfig",
    # 3rd-party apps that lms depends on
    "widget_tweaks",
    "haystack",
    "treebeard",
    "django_tables2",
]


default_app_config = "lms.config.Shop"


__version__ = get_version()
