# djeoloader
Small django app for loading gazetteer type data
The geo_import tool is designed to aid with the import of gazetteer type tabular data in CSV or text form.

Pre requisites.
1. Spatially enabled database
2. GEOS libraries

The import_gazetteer function should be run from within a django shell


KWARGS to import_gazetteer:

1.source (mandatory, string path to import file)
2.epsg (optional, numeric, espg/srid code for projection of data, defaults to 4326)
3.feature_type (mandatory, numeric, the column index where the type descriptor is stored)
4.delimiter (optional, string, defaults to ",")
5.quote (optional, string, defaults to '"')
6. x or lng (mandatory, numeric, the column index of the x coordinate)
7. y or lat (mandatory, numeric, the column index of the y coordinate)


ARGS to import gazetteer:

Non keyword arguments are the numeric indices of columns containing the heirarchical data names.
UP TO 5 levels of hierarchy are currently supported.

The order of the ARGS *MUST* be in ascending order of precision
e.g. (3,5,6,...) : where 3 might be the country index, 5 might be a county, and 6 might be the index of the 
individual placename.

PROCESS:

1. Add "geos_base" to your applications list of INSTALLED_APPS

2.run ./manage.py syncdb to create the default tables in the database

By default, tables GeoHierarchy1...5 are created. 
It is recommended that following import that you set verbose_name and verbose_name_plural properties in
the object's class Meta: for human readable descriptions

3. Copy your source file to a location local to the server

4. run ./manage.py shell

5. from geos_base.geo_import import *

6. run import_gazetteer(args[n,n,n,n,n],kwargs[source='/path/to/file',delimiter=',',quote='"',epsg=[epsg code],x(or lng)=n,y(or lat)=n,feature_type=n)

import_gazetteer reads the source csv a line at a time and creates new FeatureTypes as requested.
It is recommended that after import, the FeatureType model may need to be amended to to add human readable descriptions
if feature type codes have been imported

High level hierarchical objects are created initially, and the script checks for duplicate names during import.
Lower level hierarchical objects are assigned parents as appropriate and only the lowet level objects may have coordinates.

Regardless of original SRID, all points are transformed to ESPG:4326 being standard WGS84 coordinates.












