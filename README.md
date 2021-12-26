# usgs-dem-geojson

CURRENTLY BROKEN! USGS changed directory structure and the links no longer work...

This will read through the available 10m DEMs from the USGS, sort by most recent for each quad, and create a GeoJSON of the footprints with the download link.

The default is to use the AWS Docker container to query S3. If you have the AWS cli insalled locally, change "USE_DOCKER = True" to "USE_DOCKER = False".
