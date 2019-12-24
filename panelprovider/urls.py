from django.contrib import admin
from django.urls import include
from django.conf.urls import url
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    url(r'^', include('task.urls')),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)