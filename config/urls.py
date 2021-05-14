from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token
from django.views.decorators.csrf import csrf_exempt
from djgumroad.products.views import (
    ProductListView, 
    UserProductListView,
    ProductCreateView,
    CreateCheckoutSessionView,
    SuccessView,
    stripe_webhook,
)
from djgumroad.users.views import UserProfileView

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("discover/", ProductListView.as_view(), name='discover'),
    path('products/', UserProductListView.as_view(), name='user-products'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('profile/', UserProfileView.as_view(), name="profile"),
    path("p/", include('djgumroad.products.urls', namespace='products')),
    path("create-checkout-session/<slug>/", CreateCheckoutSessionView.as_view(), name="create-checkout-session"),
    path('success/', SuccessView.as_view(), name='success'),
    path("webhooks/stripe/", stripe_webhook, name='stripe-webhook'),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("djgumroad.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns