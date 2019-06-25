from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from modules.core.views import PageNotFoundView, PageServerErrorView

handler404 = PageNotFoundView.as_view()
handler500 = PageServerErrorView.as_view()

urlpatterns = [
    path('', include('modules.core.urls')),
    path('admin/', admin.site.urls),
    path('admin_tools/', include('admin_tools.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('captcha/', include('captcha.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
