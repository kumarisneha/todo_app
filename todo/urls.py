"""todo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from todoapp import views

urlpatterns = [
	url(r'^$', views.home),
    url(r'^registration/$', views.registration_page),
    url(r'^reset_password/(?P<code>.*)/$', views.forgot_pass_verify),
    url(r'^verification/(?P<code>.*)/$', views.verify),
    url(r'^login/$', views.login_page),
    url(r'^logout/$', views.logout),
    url(r'^login_verify/$',views.login_valid),
	url(r'^delete/(\d+)/$',views.delete_item),	
	url(r'^delete_all/$',views.delete_all),
    url(r'^update/(\d+)/$',views.update_list),
    url(r'^new_password/$',views.new_passwd),
    url(r'^forgot_password/$',views.forgot_password),
    url(r'^notification_setting/$',views.email_notification),
    url(r'^newpage/(\d+)/$',views.newpage),
    url(r'^admin/', admin.site.urls),
]
