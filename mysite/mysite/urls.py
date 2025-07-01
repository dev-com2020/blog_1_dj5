
from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')),
] + debug_toolbar_urls()
