import os
import glob
import json
from datetime import date

USE_DOCKER = True

def read_s3_10m():
    cmd = 'aws s3 ls  --no-sign-request --recursive s3://prd-tnm/StagedProducts/Elevation/13/TIFF/current | grep -e ".tif" > 10mTIFF.txt'
    if USE_DOCKER:
        cmd = 'docker run -it amazon/aws-cli s3 ls  --no-sign-request --recursive s3://prd-tnm/StagedProducts/Elevation/13/TIFF/current | grep -e ".tif" > 10mTIFF.txt'
    os.system(cmd)


def read_usgs_list(dem_list):
    with open(dem_list,'r') as dl:
        lines = dl.readlines()
    dem_dict = {}
    for line in lines:
        line = line.split()
        print(line)
        load_date = line[0]
        the_quad = line[3].split('/')[5]
        the_tif = line[3].split('/')[6]
        dem_dict[the_quad] = the_tif, load_date
    return dem_dict

def make_geojson(available_dems):
    fpName = 'USGS-dem-footprints'
    the_date = date.today().strftime("%Y-%m-%d")
    features = []
    loop = 0
    for k in available_dems:
        the_tif, load_date = available_dems[k]
        ns = -1
        if k[0] == 'n':
            ns = 1
        ew = -1
        if k[3] == 's':
            ew = 1
        lat = int(k[1:3]) * ns
        lon = int(k[4:7]) * ew
        ul_lon = lon
        ul_lat = lat
        ur_lon = lon + 1
        ur_lat = lat
        lr_lon = lon + 1
        lr_lat = lat - 1
        ll_lon = lon
        ll_lat = lat - 1
        #print(k[0], ns, lat, k[3], ew, lon, lon, lat)
        #print(ul, ll, lr, ur, ul)
        feat = {}
        feat['type'] = 'Feature'
        feat['id'] = loop
        prop = {}
        prop['Name'] = k
        prop['URL'] = 'http://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/13/TIFF/current/%s/%s' % (k, the_tif)
        prop['Extracted'] = the_date
        prop['LoadDate'] = load_date
        #prop['Description']=basename
        feat['properties'] = prop
        geo = {}
        geo['type']='Polygon'
        coordArr = [[ll_lon,ll_lat],[lr_lon,lr_lat],[ur_lon,ur_lat],[ul_lon,ul_lat],[ll_lon,ll_lat]]
        #print coordArr
       
        geo['coordinates']=[coordArr]
        feat['geometry']=geo
        features.append(feat)
        loop += 1

    thePoly = '%s.geojson' % fpName
    wfile = open(thePoly,'w')
    jsonstr = {}
    jsonstr['type'] = 'FeatureCollection'
    #jsonstr['extrac_date'] = the_date
    jsonstr['features'] = features
    json.dump(jsonstr,wfile)
    wfile.flush()
    wfile.close()

read_s3_10m()
available_dems = read_usgs_list('10mTIFF.txt')
make_geojson(available_dems)
