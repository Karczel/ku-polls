from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

from polls import views

urlpatterns = [
    path('', RedirectView.as_view(url='/polls/', permanent=False)),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup')
]
