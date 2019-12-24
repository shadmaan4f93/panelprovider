from django.db import models
from django.contrib.auth.models import User


class PanelProvider(models.Model):
    code = models.CharField(max_length=200,default=None, null=True,blank=False)

    def __str__(self):
        return self.code


class Country(models.Model):
    name = models.CharField(max_length=200, blank=False , null=False)
    country_code = models.CharField(max_length=200,default=None, null=True,blank=False)
    panel_provider_id = models.ForeignKey(PanelProvider,related_name='countries',null=True,blank=False,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name


class LocationGroup(models.Model):
    name = models.CharField(max_length=200, blank=False , null=False)
    country_id = models.ForeignKey(Country,related_name='locationgroups',null=True,on_delete=models.CASCADE)
    panel_provider_id = models.ForeignKey(PanelProvider,related_name='locationgroups',null=True,blank=False,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=200, blank=False , null=False)
    secret_code = models.CharField(max_length=200,default=None, null=True,blank=False)
    external_id = models.ForeignKey(LocationGroup,related_name='locations',default=None,null=True,blank=False,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TargetGroup(models.Model):
    name = models.CharField(max_length=200, blank=False , null=False)
    parent_id = models.ForeignKey('self',related_name='subtargetgroups',on_delete=models.CASCADE,null=True,blank=True)
    external_id = models.ForeignKey(Country,related_name='targetgroups',null=True,blank=True,on_delete=models.CASCADE)
    secret_code = models.CharField(max_length=200,default=None, null=True,blank=False)
    panel_provider_id = models.ForeignKey(PanelProvider,null=True,blank=False,on_delete=models.CASCADE)

    def __str__(self):
        return self.name




