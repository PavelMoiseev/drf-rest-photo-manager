from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from photo_manager_app.views import *
from users.views import *


urlpatterns = [
    path('', ApiOverview.as_view()),
    path('display-and-upload/', MainImages.as_view()),
    path('select-and-delete/<str:pk>', SelectImage.as_view()),
    path('update-image/<str:pk>', UpdateImage.as_view()),
    path('admin/', admin.site.urls),
    path('api-auth', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('registr/', RegistrUserView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
