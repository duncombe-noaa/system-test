
# coding: utf-8

# Outline of Notebook Elements:
# *  Theme Title
# *  Questions
# *  DISCOVERY Process (code and narrative)
# *  ACCESS Process (code and narrative)
# *  USE Process (code and narrative)
# *  Results and Conclusions (narrative)

## Theme: Baseline Question: What Model records and how many are available via each endpoint?

# In[7]:

#Import the libraries we think we need
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
from numpy import random
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import csv
import re
import cStringIO
import urllib2
import parser
import pdb
#import iris
import random
import datetime as dt
from datetime import datetime
from pylab import *
from owslib.csw import CatalogueServiceWeb
from owslib.wms import WebMapService
from owslib.csw import CatalogueServiceWeb
from owslib.sos import SensorObservationService
from owslib.etree import etree
from owslib import fes
import netCDF4
import SPARQLWrapper
from SPARQLWrapper import SPARQLWrapper, JSON


# In[8]:

#This cell lists Catalog Service for the Web endpoints. As CSW's are discovered within the larger
#    IOOS Umbrella, this list is updated by the IOOS Program Office here:
#    https://github.com/ioos/system-test/wiki/Service-Registries-and-Data-Catalogs

#endpoint = 'http://data.nodc.noaa.gov/geoportal/csw'  # NODC Geoportal: collection level
#endpoint = 'http://geodiscover.cgdi.ca/wes/serviceManagerCSW/csw'  # NRCAN 
#endpoint = 'http://geoport.whoi.edu/gi-cat/services/cswiso' # USGS Woods Hole GI_CAT
#endpoint = 'http://cida.usgs.gov/gdp/geonetwork/srv/en/csw' # USGS CIDA Geonetwork
#endpoint = 'http://www.nodc.noaa.gov/geoportal/csw'   # NODC Geoportal: granule level
#endpoint = 'http://cmgds.marine.usgs.gov/geonetwork/srv/en/csw'  # USGS Coastal & Marine Program Geonetwork
#endpoint = 'http://www.ngdc.noaa.gov/geoportal/csw' # NGDC Geoportal
#endpoint = 'http://www.ncdc.noaa.gov/cdo-web/api/v2/' #NCDC CDO Web Services
#endpoint = 'http://geo.gov.ckan.org/csw' #CKAN Testing Site for new Data.gov
#endpoint = 'https://edg.epa.gov/metadata/csw' #EPA
#endpoint = 'http://geoport.whoi.edu/geoportal/csw' #WHOI Geoportal
#endpoint = 'http://cwic.csiss.gmu.edu/cwicv1/discovery' #CWIC
#endpoint = 'http://portal.westcoastoceans.org/connect/' #West Coast Governors Alliance (Based on ESRI Geoportal back end
#endpoint = 'http://gcmdsrv.gsfc.nasa.gov/csw' #NASA's Global Change Master Directory (GCMD) CSW Service (Requires Authorization)
#endpoint = 'http://gcmdsrv3.gsfc.nasa.gov/csw' #NASA's Global Change Master Directory (GCMD) CSW Service (Requires Authorization)
#endpoint = 'https://data.noaa.gov/csw' #data.noaa.gov csw

endpoints = ['http://www.nodc.noaa.gov/geoportal/csw',
             'http://www.ngdc.noaa.gov/geoportal/csw',
             'http://catalog.data.gov/csw-all',
             'http://cwic.csiss.gmu.edu/cwicv1/discovery',
             'http://geoport.whoi.edu/geoportal/csw',
             'https://edg.epa.gov/metadata/csw',
             'http://cmgds.marine.usgs.gov/geonetwork/srv/en/csw',
             'http://cida.usgs.gov/gdp/geonetwork/srv/en/csw',
             'http://geodiscover.cgdi.ca/wes/serviceManagerCSW/csw', 
             'http://geoport.whoi.edu/gi-cat/services/cswiso']


# In[6]:

#This is a collection of lists that we will need to examine Catalogs
variables = ['phytoplankton','zooplankton', 'fish', 'river', 'currents', 'bathymetry', 'wind']
std_name_list=['water_surface_height_above_reference_datum',
    'sea_surface_height_above_geoid','sea_surface_elevation',
    'sea_surface_height_above_reference_ellipsoid','sea_surface_height_above_sea_level',
    'sea_surface_height','water level']
dap_strings = ['urn:x-esri:specification:ServiceType:odp:url', 'urn:x-esri:specification:ServiceType:OPendap:url']
model_strings = ['roms','selfe','adcirc','ncom','hycom','fvcom']
# This looks like a good notebook to work from
# https://www.wakari.io/sharing/bundle/rsignell/Model_search


# In[4]:

def service_urls(records,service_string='urn:x-esri:specification:ServiceType:odp:url'):
    urls=[]
    for key,rec in records.iteritems():
        #create a generator object, and iterate through it until the match is found
        #if not found, gets the default value (here "none")
        url = next((d['url'] for d in rec.references if d['scheme'] == service_string), None)
        if url is not None:
            urls.append(url)
    return urls



# In[5]:

#This cell examines and provides information on the number of model records
#   available via each catalog endpoint
records1 = []
titles1 = []
lenrecords1 = []
lentitles1 = []
k = 0
for endpoint in endpoints[:3]:    
    csw = CatalogueServiceWeb(endpoint,timeout=60)
    for model_string in model_strings:
        try:
            csw.getrecords(keywords = [model_string], maxrecords = 60, esn = 'full')
            records1.append(csw.results)
        except Exception, ex1:
            records1.append('Error')
        try:
            for rec in csw.records:    
                titles1.append(csw.records[rec].title)
        except Exception, ex1:    
                titles1.append('Error')  
        lentitles1.append(len(titles1[-1]))
        lenrecords1.append(len(records1[-1]))

zipvar1 = zip(endpoints, records1,lenrecords1, titles1,lentitles1)
df = DataFrame(data = zipvar1, columns = ['endpoints', 'records1','lenrecords1', 'titles1','lentitles1'])
df.head()


# In[28]:

#this cell attempts to access the pertinent PMEL-run Model Forecasts for the Bering Sea
records1 = []
titles1 = []
lenrecords1 = []
lentitles1 = []
model_strings = ['ECHO-G',
                 'CCCma',
                 'MIROC',
                 'FORECAST',
                 'NCEP CFS-R',
                 'CLIVAR']

for endpoint in endpoints[:3]:    
    csw = CatalogueServiceWeb(endpoint,timeout=60)
    for model_string in model_strings:
        try:
            csw.getrecords(keywords = [model_string], maxrecords = 60, esn = 'full')
            records1.append(csw.results)
        except Exception, ex1:
            records1.append('Error')
        try:
            for rec in csw.records:    
                titles1.append(csw.records[rec].title)
        except Exception, ex1:    
            titles1.append('Error') 
        #lentitles1.append(len(titles1[-1]))
        #lenrecords1.append(len(records1[-1]))

zipvar1 = zip(model_strings,endpoints, records1, titles1)
df = DataFrame(data = zipvar1, columns = ['model','endpoints', 'records1', 'titles1'])
df.head()


# In[23]:

df.ix[:3]['titles1']


# In[29]:

#This Cell will examine the areas of interest under the Important Bird Areas Identified in the following document,
#ak.audubon.org/sites/default/files/documents/marine_ibas_report_final_sep_2012.pdf (at Section 1.3 Study Areas)

#Establish fes_date_filter definitions
def fes_date_filter(start_date='1900-01-01',stop_date='2100-01-01',constraint='overlaps'):
    if constraint == 'overlaps':
        start = fes.PropertyIsLessThanOrEqualTo(propertyname='apiso:TempExtent_begin', literal=stop_date)
        stop = fes.PropertyIsGreaterThanOrEqualTo(propertyname='apiso:TempExtent_end', literal=start_date)
    elif constraint == 'within':
        start = fes.PropertyIsGreaterThanOrEqualTo(propertyname='apiso:TempExtent_begin', literal=start_date)
        stop = fes.PropertyIsLessThanOrEqualTo(propertyname='apiso:TempExtent_end', literal=stop_date)
    return start,stop

#Establish bounding box filter for Geographic Range of IBAs
bbox = fes.BBox([-130.5, 47.9, 167.6, 74.7])


# In[50]:

sparql = SPARQLWrapper("http://mmisw.org/sparql")
queryString = """
PREFIX ioos: <http://mmisw.org/ont/ioos/parameter/>
SELECT DISTINCT ?parameter ?definition ?unit ?property ?value 
WHERE {?parameter a ioos:Parameter .
       ?parameter ?property ?value .
       ?parameter ioos:Term ?term . 
       ?parameter ioos:Definition ?definition . 
       ?parameter ioos:Units ?unit .
       FILTER (regex(str(?property), "(exactMatch|closeMatch)", "i") && regex(str(?value), "temperature", "i") )
      } 
ORDER BY ?parameter
"""

sparql.setQuery(queryString)
sparql.setReturnFormat(JSON)
j = sparql.query().convert()

j.keys()

j["head"]["vars"]


# In[64]:

j
dict = j
print j


# In[38]:

#This Cell will access the catalogs for the variables pertinent to the PMEL Models within the set Geographic Range

variables = ['sea_surface_temperature',
             'sea_water temperature', 
             'fish', 
             'river', 
             'currents', 
             'bathymetry', 
             'wind']
variables1 = []
records1 = []
titles1 = []
lenrecords1 = []
lentitles1 = []

for endpoint in endpoints[:3]:
    csw = CatalogueServiceWeb(endpoint,timeout=60)
    for v in variables[:2]:
        try:
            csw.getrecords(keywords = [v], maxrecords = 60, esn = 'full')
            records1.append(csw.results)
        except Exception, ex1:
            records1.append('Error')
        try:
            for rec in csw.records:    
                titles1.append(csw.records[rec].title)
        except Exception, ex1:
            titles1.append('Error') 
    lentitles1.append(len(titles1[-1]))
    lenrecords1.append(len(records1[-1]))

zipvar1 = zip(endpoints, records1,lenrecords1, titles1,lentitles1)
df = DataFrame(data = zipvar1, columns = ['endpoints','records1','lenrecords1', 'titles1','lentitles1'])
df.head()
#df.groupby([variables1])


# In[ ]:



