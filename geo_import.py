#######



#######

from geo_models import *

from django.contrib.gis.geos import GEOSGeometry,Point


import csv

### Typical string might be (from OS Gazetteer):
### Using std input 1:NB5464:A' Beirghe:NB46:58:30:6:12.9:964500:154500:W:WI:N Eil:Na h-Eileanan an Iar:X:21-JAN-2003:U:8:0:0
### import_gazetteer(13,2,source='/path/to/csv/file/gaz_sample.csv',epsg=27700,x=9,y=8,feature_type=14,delimiter=':')

def import_gazetteer(*args,**kwargs):
    ###
    # args in order give column numbers of
    # heirarchy names e.g. 3,5,6 =
    # 3 tiers, 6th column being most precise
    # then, 5th and then 3th being braodest classification
    # Set up default kwargs
    # csv source
    ###
    source = kwargs.get('source','')
    # projection
    epsg = kwargs.get('epsg',4326)
    # y column from csv
    y = kwargs.get('y','lat')
    # x column from csv
    x = kwargs.get('x','lng')
    # feature type column from csv (column number)
    feature_type = kwargs.get('feature_type',0)
    # delimiter
    delimiter = kwargs.get('delimiter',',')
    quote = kwargs.get('quote','"')
    # if no source then abort
    if source == '':
        return 'You must specify a file source'
    #else:
    #    import csv
    # Establish hierarchy levels from args
    hierarchies = args.__len__()
    if hierarchies > 5:
        return 'Import function supports 5 levels of place hierarchy by default.'
    if hierarchies == 0:
        return 'Import function requres at least one column from source designated as\
             a source of a hierarchical level.'
    # Collect feature types for comparison
    feature_types = []
    currParent = None
    with open(source,'rb') as csvfile:
        gazetteer_reader = csv.reader(csvfile,delimiter=delimiter\
            ,quotechar=quote)
        for row in gazetteer_reader:
            # Reset the hierarchies counter
            currHier = hierarchies
            if row[feature_type] not in feature_types:
                feature_types.append(row[feature_type])
                ftype = FeatureType()
                ftype.name = row[feature_type]
                ftype.save()
            # Import hierarchical levels
            for h in args:
                print row[0]
                currHierarchyObjectStr = u'GeoHierarchy%s' % ( str( currHier ) )
                if eval(currHierarchyObjectStr).objects.filter(name=row[h]).__len__() > 0 and currHier != 1:
                    currParent = eval(currHierarchyObjectStr).objects.filter(name=row[h])[0]               
                elif eval(currHierarchyObjectStr).objects.filter(name=row[h]).__len__() == 0 or currHier == 1: 
                    hier = eval(currHierarchyObjectStr)()
                    hier.name = row[h]
                    if currParent and (hier != currParent):
                        hier.parent = currParent                 
                    # Store this as the parent or the next hierarchical object
                    if currHier != 1: # It's going to be the parent of something...
                        currParent = hier
                    else:
                        currParent = None
                    if currHier == 1:
                        hier.feature_type = FeatureType.objects.get(name=row[feature_type])
                        pointStr = u'POINT (%s %s)' % (str(row[x]),str(row[y]))
                        point = GEOSGeometry(pointStr,srid=epsg)
                        point.transform(4326)
                        hier.point = point
                    hier.save()
                if currHier > 1:
                    currHier = currHier - 1













