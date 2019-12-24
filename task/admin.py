from django.contrib import admin
from .models import LocationGroup,Location,PanelProvider,Country,TargetGroup

admin.site.register(LocationGroup)
admin.site.register(Location)
admin.site.register(PanelProvider)
admin.site.register(Country)
admin.site.register(TargetGroup)
