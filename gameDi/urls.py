from django.conf import settings
from django.conf.urls.static import static
from allauth.account import views as v
from django.contrib import admin
from django.urls import path, include

from gameDi import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jet', include('jet.urls', 'jet')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('', include('allauth.urls')),
    path('', v.login, name="account_login"),
    path('', include('base.urls'))

   # path('', views.logout_view, name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
