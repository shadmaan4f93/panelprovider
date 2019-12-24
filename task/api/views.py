import json
import requests
import urllib.request
from django.http import HttpResponse
from bs4 import BeautifulSoup
from inscriptis import get_text
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from panelprovider.settings import logger

from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from task.models import (
    Location,
    TargetGroup,
    LocationGroup,
    TargetGroup,
    Country,
    PanelProvider
)

from task.api.serializers import (
    LocationSerializer,
    TargetGroupSerializer,
    PanelProviderSerializer,
    LocationGroupSerializer,
    CountrySerializer,
    CountryTargetGroupSerializer,
    TargetWithSubtargetSerializer
)

#---------------------------------------------------------------------------------------

class LocationByCountryCodePrivateAPI(RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CountrySerializer
    lookup_field = 'country_code'
    queryset = Country.objects.all()


class TargetGroupByCountryCodePrivateApi(RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CountryTargetGroupSerializer
    lookup_field = 'country_code'
    queryset = Country.objects.all()

#-------------------------------------------------------------------------------------

class LocationByCountryCodePublicAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = CountrySerializer
    lookup_field = 'country_code'
    queryset = Country.objects.all()

class TargetGroupByCountryCodePublicApi(RetrieveUpdateDestroyAPIView):
    serializer_class = CountryTargetGroupSerializer
    lookup_field = 'country_code'
    queryset = Country.objects.all()

class GetPanelPrice(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,country_code,target_group_id):
        """ This function used to calculate panel Provider price.

        Args:
        request (dict): HttpRequest Object coming with the browser request |
        country_code (str): country_code is an attribute of the country |
        target_group_id(int):Unique identifier for a TargetGroup |

        Returns:
        dict: ({"results":{"panel":panelcode,"price":price},"status":STATUS_CODES}) The return value. """
        try:
            return_value = {
                "status": None,
                "results": None
            }
            try:
                country = Country.objects.get(country_code=country_code)
            except:
                return_value["status"] = 404
                return_value["results"] = {}
                logger.info("Invalid Country code Provides --{}".format(country_code))
                return Response(return_value)
            try:
                targetgroup = TargetGroup.objects.get(id=target_group_id,panel_provider_id=country.panel_provider_id)
            except:
                subtargetgroup = TargetGroup.objects.get(id=target_group_id)
                if subtargetgroup:
                    if subtargetgroup.parent_id_id :
                        try:
                           targetgroup = TargetGroup.objects.get(id=subtargetgroup.parent_id_id,panel_provider_id=country.panel_provider_id)
                        except Exception as e:
                            return_value["status"] = 404
                            return_value["results"] = {}
                            logger.info("Invalid TargetGroupId Provided --{}".format(target_group_id))
                            return Response(return_value)
                    else:
                        return_value["status"] = 404
                        return_value["results"] = {}
                        logger.info("Invalid TargetGroupId Provided --{}".format(target_group_id))
                        return Response(return_value)
            
            panel = PanelProvider.objects.filter(id=targetgroup.panel_provider_id_id).values("code")
            panelcode = panel[0]["code"]
            PanelPriceObj=PanelPricing()
            price = PanelPriceObj.execute(panelcode)
            if price is not None:
                return_value["status"] = 200
                return_value["results"] = {"panel": panel[0]["code"], "price":price}
                logger.info("panel price calculated succesfully %s",repr(return_value))
            else:
                return_value["status"] = 500
                return_value["results"] = {}
                logger.info("panel price not calculated due to internal server error")
        except Exception as e:
            return_value["status"] = 500
            return_value["results"] = {}
            logger.error("error",repr(e))

        return Response(return_value)

class PanelPricing():

    def execute(self,method):
        try:
            method = getattr(self,method,lambda: 'Invalid')
            return method()
        except Exception as e:
            return 'Invalid'
    

    def pn1(self):
        """  This Function calculates The total occurance of letter 'a' on a site 'http://time.com'.  
             Using urllib to fetch html contents and extracting text with inscripts.add()
             Finally The Price is Calculated By dividing total count by 100 """
        try:
            price = None
            url = 'http://time.com'
            html = urllib.request.urlopen(url).read().decode('utf-8')
            text = get_text(html)
            count = sum(map(lambda x : 1 if 'a' in x else 0, text))
            price = count/100
        
        except Exception as e:
            price =None
        
        return price

    def pn2(self):
        """ This Function Calculates The Panel Price By Counting All the Arrays Containing More Than 10 Items 
            From The Results Fetched By 'http://openlibrary.org/search.json?q=the+lord+of+the+rings' """
                                                             
        url = 'http://openlibrary.org/search.json?q=the+lord+of+the+rings'
        html = urllib.request.urlopen(url).read().decode('utf-8')
        data = json.loads(html)
        count = 0
        price = None
        try:
            for doc in data["docs"]:
                if type(doc) is dict:
                    for k,v in doc.items():
                        if type(v) is list:
                            if len(v) >10:
                                count = count +1
            price = count

        except:
            price = None
            
        return price

    def pn3(self):
        """  This Function Calculates Panel Provider Price By counting Total Number Of Tags Present
              On The Site 'http://time.com' And Dividing It By 100.This Function Uses requests and  BeautifulSoup."""
        try:
            price = None
            url = 'http://time.com'
            content = requests.get(url)
            soup = BeautifulSoup(content.text, 'html.parser')
            t = [tag.name for tag in soup.find_all()]
            price =len(t)/100
        except:
            price = None
        
        return price






class GetTargetGroupsByCountryCode(ListAPIView):
    serializer_class = CountryTargetGroupSerializer
    queryset = Country.objects.all()




class CountryListAPIView(ListAPIView):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()





class PanelProviderCreateAPIView(CreateAPIView):
    serializer_class = PanelProviderSerializer
    queryset = PanelProvider.objects.all()


class PanelProviderListAPIView(ListAPIView):
    serializer_class = PanelProviderSerializer
    queryset = PanelProvider.objects.all()


class CountryCreateAPIView(CreateAPIView):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()

class LocationGroupCreateAPIView(CreateAPIView):
    serializer_class = LocationGroupSerializer
    queryset = LocationGroup.objects.all()


class LocationGroupListAPIView(ListAPIView):
    serializer_class = LocationGroupSerializer
    queryset = LocationGroup.objects.all()


class LocationCreateAPIView(CreateAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()


class LocationListAPIView(ListAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

class TargetGroupCreateAPIView(CreateAPIView):
    serializer_class = TargetGroupSerializer
    queryset = TargetGroup.objects.all()


class TargetGroupListAPIView(ListAPIView):
    serializer_class = TargetGroupSerializer
    queryset = TargetGroup.objects.all()

class TargetGroupWithSubTargetListAPIView(ListAPIView):
    serializer_class = TargetWithSubtargetSerializer
    queryset = TargetGroup.objects.all()