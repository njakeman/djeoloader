from django.contrib.gis.db import models

class FeatureType(models.Model):
    name = models.CharField(max_length=64)
    # Add custom field here if needed ...
    # Name will be used for importing values
    objects = models.GeoManager()
    def __unicode__(self):
        return u'%s' % self.name

class GeoHierarchy5(models.Model):
    name = models.CharField(max_length=64)
    objects = models.GeoManager()	
    def __unicode__(self):
        return u'%s' % self.name    
    class Meta:
        ordering = ('name',)        
	
class GeoHierarchy4(models.Model):
    name = models.CharField(max_length=64)
    parent =  models.ForeignKey('GeoHierarchy5',null=True,blank=True)
    objects = models.GeoManager()	
    def __unicode__(self):
        return u'%s' % self.name    
    class Meta:
        ordering = ('name',)        

class GeoHierarchy3(models.Model):
    name = models.CharField(max_length=64)
    parent =  models.ForeignKey('GeoHierarchy4',null=True,blank=True)
    objects = models.GeoManager()
    def __unicode__(self):
        return u'%s' % self.name    
    class Meta:
        ordering = ('name',)        

class GeoHierarchy2(models.Model):
    name = models.CharField(max_length=64)
    parent =  models.ForeignKey('GeoHierarchy3',null=True,blank=True)
    objects = models.GeoManager()
    def __unicode__(self):
        return u'%s' % self.name
    class Meta:
        ordering = ('name',)        

class GeoHierarchy1(models.Model):
    name = models.CharField(max_length=64)
    parent =  models.ForeignKey('GeoHierarchy2',null=True,blank=True)
    point = models.PointField(srid=4326,null=True,blank=True)
    feature_type = models.ForeignKey('FeatureType',null=True,blank=True)
    objects = models.GeoManager()
    def __unicode__(self):
        return u'%s' % self.name
    class Meta:
        ordering = ('name',)