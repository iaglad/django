"""students_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

# from students import views as stud_views
from students.views import students, groups, journal, contact_admin

urlpatterns = [
    # students urls
    path('', students.students_list, name='home'),
    path('students/add/', students.StudentCreateView.as_view(), name='students_add'),
    path('students/<int:pk>/edit/', students.StudentUpdateView.as_view(), name='students_edit'),
    path('students/<int:pk>/delete/', students.StudentDeleteView.as_view(), name='students_delete'),
    # groups urls
    path('groups/', groups.groups_list, name='groups'),
    path('groups/add/', groups.GroupCreateView.as_view(), name='groups_add'),
    path('groups/<int:pk>/edit/', groups.GroupUpdateView.as_view(), name='groups_edit'),
    path('groups/<int:pk>/delete/', groups.GroupDeleteView.as_view(), name='groups_delete'),
    # journal urls
    path('journal/', journal.journal, name='journal'),
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico'), name='favicon'),
    path('admin/', admin.site.urls),
    path('contact-admin/', contact_admin.ContactView.as_view(), name='contact_admin'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
