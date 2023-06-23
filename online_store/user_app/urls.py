from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'user_app'

urlpatterns = [
                  path('login', views.user_login, name='login'),
                  path('logout', views.Logout.as_view(), name='logout'),
                  path('registration', views.registration, name='registration'),
                  path('lk', views.PersonalPage.as_view(), name='personal_page'),
                  path('lk/edit', views.edit_profile, name='edit_profile'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
