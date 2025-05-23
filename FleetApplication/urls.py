from django.contrib import admin
from django.urls import path,include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf.urls.static import static
from django.conf import settings
from general.views import privacy_policy

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/user/',include('user.urls')),
    path('api/fleet/',include('fleet.urls')),

    path('api/general/',include('general.urls')),

    path('api/job/',include('jobs.urls')),
]


urlpatterns += [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path("privacy_policy/", privacy_policy, name="privacy_policy"),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)