from django.contrib.gis.db import models

from geo_models import *

class GisModel(models.Model):
    name = models.CharField(max_length=64)
    objects = models.GeoManager()

    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains",)

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'{name}'.format(name=self.name)


class GisMultiPolygonModel(GisModel):
    geo = models.MultiPolygonField()

    class Meta:
        abstract = True


class GisPointModel(GisModel):
    geo = models.PointField(blank=True, null=True)

    class Meta:
        abstract = True


class Country(GisMultiPolygonModel):
    class Meta:
        verbose_name_plural = 'Countries'


class County(GisMultiPolygonModel):
    country = models.ForeignKey(Country)

    class Meta:
        unique_together = ('country', 'name')
        verbose_name_plural = 'Counties'


class FeatureType(models.Model):
    code = models.CharField(max_length=8, unique=True)
    description = models.CharField(max_length=256)
    created = models.DateTimeField('date created', auto_now_add=True)
    modified = models.DateTimeField('date modified', auto_now=True)

    class Meta:
        verbose_name_plural = 'Feature Types'


class City(GisPointModel):
    county = models.ForeignKey(County)
    feature = models.ForeignKey(FeatureType, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Cities'


class Venue(GisPointModel):
    city = models.ForeignKey(City)

    class Meta:
        unique_together = ('city', 'name')
