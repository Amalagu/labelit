from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

app_name = "label"

urlpatterns = [


	]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
