"""telco_ui URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, patterns, include
from django.contrib import admin
from telco_service.Views.CampaignViews import CampaignStatsViewSet, OverllStatsViewSet, CampaignReportViewSet
from telco_service.Views.AgeStatsViews import AgeStatsViewSet
from telco_service.Views.GenderStatsViews import  GenderStatsViewSet
from rest_framework import routers
from telco_service import views
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^api/', include(router.urls)),
    url(r'^api/telco/v1/campaigns_list', CampaignStatsViewSet.as_view({'get': 'list'}), name='campaign_list'),
    url(r'^api/telco/v1/campaigns/', CampaignStatsViewSet.as_view({'get':'retrieve'}), name='campaign_list' ),
    url(r'^api/telco/v1/campaigns_report', CampaignReportViewSet.as_view({'get': 'retrieve'}), name='campaign_report'),
    url(r'^api/telco/v1/overall_stats/', OverllStatsViewSet.as_view({'get': 'retrieve'}), name='overall_stats'),
    url(r'^api/telco/v1/age_stats_list/', AgeStatsViewSet.as_view({'get': 'list'}), name='agestats_list'),
    url(r'^api/telco/v1/age_stats/', AgeStatsViewSet.as_view({'get': 'retrieve'}), name='agestats_retrieve'),
    url(r'^api/telco/v1/gender_stats_list/', GenderStatsViewSet.as_view({'get': 'list'}), name='genderstats_list'),
    url(r'^api/telco/v1/gender_stats/', GenderStatsViewSet.as_view({'get': 'retrieve'}), name='genderstats_retrieve'),
]
