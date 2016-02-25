from django.conf import settings as s
from django.contrib.gis import admin
from models import City, County, Country, FeatureType, Venue
from geo_models import GeoHierarchy5,GeoHierarchy4,GeoHierarchy3,GeoHierarchy2,GeoHierarchy1

class GisAdmin(admin.OSMGeoAdmin):
    default_lon = 0
    default_lat = 6850000
    default_zoom = 4
    #openlayers_url = s.OPENLAYERS_URL


class VenueAdmin(GisAdmin):
    # define the raw_id_fields
    raw_id_fields = ('city',)
    # define the autocomplete_lookup_fields
    autocomplete_lookup_fields = {
        'fk': ['city'],
    }

class BasicAdmin(GisAdmin):
    list_display = ['name','parent',]
class BasicAdminNoParent(GisAdmin):
    pass
    
admin.site.register(City, GisAdmin)
admin.site.register(County, GisAdmin)
admin.site.register(Country, GisAdmin)
admin.site.register(FeatureType)
admin.site.register(Venue, VenueAdmin)

admin.site.register(GeoHierarchy5,BasicAdminNoParent)
admin.site.register(GeoHierarchy4,BasicAdmin)
admin.site.register(GeoHierarchy3,BasicAdmin)
admin.site.register(GeoHierarchy2,BasicAdmin)
admin.site.register(GeoHierarchy1,BasicAdmin)