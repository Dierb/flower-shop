from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .yasg import ulrpatterns as doc_urls
from products import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("cart.urls")),
    path('', include("products.urls")),
    path('api/v1/users/', include('users.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += doc_urls
