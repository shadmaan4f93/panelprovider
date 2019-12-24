from django.conf.urls import url
from . import views
from .api import views as api_views


urlpatterns = [
    url(r'^$',  views.home, name='home'),
    url(
        regex=r'^api/public/location/(?P<country_code>[\w\-]+)/$',
        view=api_views.LocationByCountryCodePublicAPI.as_view(),
    ),
    url(
        regex=r'^api/public/targetgroup/(?P<country_code>[\w\-]+)/$',
        view=api_views.TargetGroupByCountryCodePublicApi.as_view(),
    ),
    url(
        regex=r'^api/private/location/(?P<country_code>[\w\-]+)/$',
        view=api_views.LocationByCountryCodePrivateAPI.as_view(),
    ),
    url(
        regex=r'^api/private/targetgroup/(?P<country_code>[\w\-]+)/$',
        view=api_views.TargetGroupByCountryCodePrivateApi.as_view(),
    ),
    url(
        regex=r'^api/panelprice/(?P<country_code>[\w\-]+)/(?P<target_group_id>[\w\-]+)/$',
        view=api_views.GetPanelPrice.as_view(),
    ),
    url(
        regex=r'^api/panels/$',
        view=api_views.PanelProviderListAPIView.as_view(),
    ),
    url(
        regex=r'^api/targetgroups/$',
        view=api_views.TargetGroupListAPIView.as_view(),
    ),
    url(
        regex=r'^api/target/subtargets/$',
        view=api_views.TargetGroupWithSubTargetListAPIView.as_view(),
    ),
    url(
        regex=r'^api/countries/$',
        view=api_views.CountryListAPIView.as_view(),
    ),
    # url(
    #     regex=r'^api/panel/create/$',
    #     view=api_views.PanelProviderCreateAPIView.as_view(),
    # ),
   
    # url(
    #     regex=r'^api/country/create/$',
    #     view=api_views.CountryCreateAPIView.as_view(),
    # ),
    # url(
    #     regex=r'^api/locationgroups/$',
    #     view=api_views.LocationGroupListAPIView.as_view(),
    # ),
    # url(
    #     regex=r'^api/locationgroup/create/$',
    #     view=api_views.LocationGroupCreateAPIView.as_view(),
    # ),
    # url(
    #     regex=r'^api/locations/$',
    #     view=api_views.LocationListAPIView.as_view(),
    # ),
    # url(
    #     regex=r'^api/location/create/$',
    #     view=api_views.LocationCreateAPIView.as_view(),
    # ),
   
    # url(
    #     regex=r'^api/targetgroup/create/$',
    #     view=api_views.TargetGroupCreateAPIView.as_view(),
    # ),
    # url(
    #     regex=r'^api/countries/targetgroups/$',
    #     view=api_views.GetTargetGroupsByCountryCode.as_view(),
    # ),
     
]