from qgis.core import QgsCoordinateReferenceSystem
import processing

# Define function for projecting and clipping datasets
def project_and_clip(
    bounding_box,
    input_file,
    output_file,
    dataset_type,
    resampling=1,
    resolution=1
):
    """
    Projects and clips vector or raster datasets to the
    study area using MGA2020 Zone 55 (EPSG:7855).

    Parameters
    ----------
    bounding_box : str or Path
        Path to study area boundary (EPSG:7855).

    input_file : str or Path
        Path to input vector or raster dataset.

    output_file : str or Path
        Path for final clipped output.

    dataset_type : str
        Either "vector" or "raster".

    resampling : int, optional
        GDAL resampling method.
        0 = Nearest neighbour
        1 = Bilinear (default)
        2 = Cubic

    resolution : float, optional
        Target raster cell size in metres.
        Default is 1 m.

    Returns
    -------
    None
        Writes processed dataset to output_file.
    """

    target_crs = QgsCoordinateReferenceSystem("EPSG:7855")

    if dataset_type == "vector":

        # Reproject vector to MGA2020 Zone 55
        reprojected = processing.run(
            "native:reprojectlayer",
            {
                "INPUT": str(input_file),
                "TARGET_CRS": target_crs,
                "CONVERT_CURVED_GEOMETRIES": False,
                "OUTPUT": "TEMPORARY_OUTPUT"
            }
        )

        # Clip vector to bounding box
        processing.run(
            "native:clip",
            {
                "INPUT": reprojected["OUTPUT"],
                "OVERLAY": str(bounding_box),
                "OUTPUT": str(output_file)
            }
        )

    elif dataset_type == "raster":

        # Reproject raster to MGA2020 at specified resolution
        reprojected = processing.run(
            "gdal:warpreproject",
            {
                "INPUT": str(input_file),
                "SOURCE_CRS": None,
                "TARGET_CRS": target_crs,
                "RESAMPLING": resampling,
                "NODATA": None,
                "TARGET_RESOLUTION": resolution,
                "DATA_TYPE": 0,
                "MULTITHREADING": False,
                "EXTRA": "",
                "OUTPUT": "TEMPORARY_OUTPUT"
            }
        )

        # Clip raster to bounding box
        processing.run(
            "gdal:cliprasterbymasklayer",
            {
                "INPUT": reprojected["OUTPUT"],
                "MASK": str(bounding_box),
                "NODATA": -9999,
                "CROP_TO_CUTLINE": True,
                "KEEP_RESOLUTION": True,
                "DATA_TYPE": 0,
                "MULTITHREADING": False,
                "EXTRA": "",
                "OUTPUT": str(output_file)
            }
        )

    else:
        raise ValueError(
            "dataset_type must be 'vector' or 'raster'"
        )

    print(f"Successfully processed: {output_file}")


#Define reclassification of raster function
def reclassify_raster(
    input_layer,
    output_layer,
    classification_table,
    range_boundaries
):
    """ 
     This function reclassifies raster values according to a supplied classification table.

    Parameters
    ----------
    input_layer : str or QgsRasterLayer
        Input raster to be reclassified.

    output_layer : str or Path
        Path and filename for the reclassified output raster.

    classification_table : list
        Reclassification table containing minimum value, maximum value,
        and new class value for each range.

    range_boundaries : int
        QGIS range boundary rule used when assigning raster values
        to classes.

    Returns
    -------
    None
    """

    processing.run(
        "native:reclassifybytable",
        {
            "INPUT_RASTER": str(input_layer),
            "RASTER_BAND": 1,
            "TABLE": classification_table,
            "NO_DATA": -9999,
            "RANGE_BOUNDARIES": range_boundaries,
            "NODATA_FOR_MISSING": True,
            "DATA_TYPE": 5,
            "OUTPUT": str(output_layer)
        }
    )


#Create function for reclassifying tasveg communities based on sensitivity 

# Import required packages
from pathlib import Path
from qgis.core import QgsRasterLayer, QgsVectorLayer
import processing


# Define vegetation rasterisation and reclassification function
def rasterise_and_reclassify_vegetation(
    input_layer,
    output_layer,
    classification_table,
    reference_raster,
    code_field="VEGCODE"
):
    """
    This function reclassifies TASVEG vegetation polygons
    according to MCDA suitability scores and converts
    the classified vector layer into a raster.

    Parameters
    ----------
    input_layer : str or Path
        Path to the input TASVEG vector dataset.

    output_layer : str or Path
        Path and filename for the output suitability raster.

    classification_table : dict
        Dictionary matching TASVEG vegetation codes
        to suitability scores from 1 to 5.

    reference_raster : str or Path
        DEM used to define raster extent, resolution
        and pixel alignment.

    code_field : str, optional
        Field containing vegetation classification codes.
        Default is "VEGCODE".

    Returns
    -------
    None
        Writes the classified vegetation raster to
        the specified output_layer.
    """

    # Load input datasets
    vegetation = QgsVectorLayer(
        str(input_layer), "TASVEG", "ogr"
    )

    dem = QgsRasterLayer(
        str(reference_raster), "DEM"
    )

    if not vegetation.isValid() or not dem.isValid():
        raise ValueError("Invalid TASVEG or DEM input layer.")

    if vegetation.fields().indexFromName(code_field) == -1:
        raise ValueError(f"Missing field: {code_field}")

    if vegetation.crs() != dem.crs():
        raise ValueError("TASVEG and DEM must have the same CRS.")

    # Check all vegetation codes have suitability scores
    codes = {
        feature[code_field]
        for feature in vegetation.getFeatures()
    }

    missing = codes - set(classification_table)

    if missing:
        raise ValueError(
            f"Unclassified vegetation codes: {sorted(map(str, missing))}"
        )

    # Build QGIS field calculator expression
    formula = "CASE\n"

    for code, score in classification_table.items():
        safe_code = str(code).replace("'", "''")
        formula += (
            f'WHEN "{code_field}" = '
            f"'{safe_code}' THEN {int(score)}\n"
        )

    formula += "ELSE NULL\nEND"

    # Add MCDA_SCORE field to temporary vector layer
    classified = processing.run(
        "native:fieldcalculator",
        {
            "INPUT": str(input_layer),
            "FIELD_NAME": "MCDA_SCORE",
            "FIELD_TYPE": 1,
            "FIELD_LENGTH": 2,
            "FIELD_PRECISION": 0,
            "FORMULA": formula,
            "OUTPUT": "TEMPORARY_OUTPUT"
        }
    )

    # Get reference DEM dimensions and extent
    extent = dem.extent()
    width = dem.width()
    height = dem.height()

    # Rasterise classified vegetation
    processing.run(
        "gdal:rasterize",
        {
            "INPUT": classified["OUTPUT"],
            "FIELD": "MCDA_SCORE",
            "BURN": 0,
            "UNITS": 0,
            "WIDTH": width,
            "HEIGHT": height,
            "EXTENT": extent,
            "NODATA": -9999,
            "INIT": -9999,
            "DATA_TYPE": 1,
            "OPTIONS": "COMPRESS=DEFLATE",
            "EXTRA": "",
            "OUTPUT": str(output_layer)
        }
    )

    print(f"Vegetation raster created: {output_layer}")

# Watercourse rasterize and reclassfication function

# Import required packages
from pathlib import Path
from qgis.core import QgsVectorLayer, QgsRasterLayer
import processing


# Define function for watercourse distance suitability
def calculate_watercourse(
    hydro_file,
    bounding_box,
    reference_raster,
    output_distance,
    output_standardised
):
    """
    This function extracts watercourse features from a
    hydrographic vector dataset, rasterises them, calculates
    Euclidean distance and reclassifies distance values into
    MCDA suitability scores from 1 to 5.

    Parameters
    ----------
    hydro_file : str or Path
        Path to the input hydrographic vector dataset
        containing watercourse features.

    bounding_box : str or Path
        Path to the study area boundary used for clipping.

    reference_raster : str or Path
        Path to the DEM defining the raster extent,
        resolution and pixel alignment.

    output_distance : str or Path
        Path and filename for the Euclidean distance raster.

    output_standardised : str or Path
        Path and filename for the reclassified watercourse
        suitability raster.

    Returns
    -------
    str
        Path to the standardised watercourse suitability raster.
    """

    # Load input hydrographic layer
    hydro_layer = QgsVectorLayer(
        str(hydro_file),
        "Hydrography",
        "ogr"
    )

    if not hydro_layer.isValid():
        raise ValueError("Hydrographic layer could not be loaded")

    # Load bounding box layer
    bounding_layer = QgsVectorLayer(
        str(bounding_box),
        "Bounding Box",
        "ogr"
    )

    if not bounding_layer.isValid():
        raise ValueError("Bounding box could not be loaded")

    # Load reference DEM
    dem_layer = QgsRasterLayer(
        str(reference_raster),
        "DEM"
    )

    if not dem_layer.isValid():
        raise ValueError("Reference DEM could not be loaded")

    # Check coordinate reference systems
    if (
        hydro_layer.crs() != dem_layer.crs()
        or bounding_layer.crs() != dem_layer.crs()
    ):
        raise ValueError(
            "All input datasets must have the same CRS"
        )

    # Find field containing the value "Watercourse"
    watercourse_field = None

    for field in hydro_layer.fields():

        field_index = hydro_layer.fields().indexOf(field.name())
        values = hydro_layer.uniqueValues(field_index)

        if any(
            str(value).strip().lower() == "watercourse"
            for value in values
        ):
            watercourse_field = field.name()
            break

    if watercourse_field is None:
        raise ValueError(
            'No field containing "Watercourse" was found'
        )

    print(f"Watercourse field: {watercourse_field}")

    # Extract only watercourse features
    watercourse_result = processing.run(
        "native:extractbyexpression",
        {
            "INPUT": hydro_layer,
            "EXPRESSION":
                f'lower(trim("{watercourse_field}")) = \'watercourse\'',
            "OUTPUT": "TEMPORARY_OUTPUT"
        }
    )

    watercourses = watercourse_result["OUTPUT"]

    if watercourses.featureCount() == 0:
        raise ValueError("No watercourse features were extracted")

    # Rasterise watercourses using reference DEM grid
    raster_result = processing.run(
        "gdal:rasterize",
        {
            "INPUT": watercourses,
            "FIELD": None,
            "BURN": 1,
            "UNITS": 0,
            "WIDTH": dem_layer.width(),
            "HEIGHT": dem_layer.height(),
            "EXTENT": dem_layer.extent(),
            "NODATA": None,
            "INIT": 0,
            "DATA_TYPE": 1,
            "EXTRA": "",
            "OUTPUT": "TEMPORARY_OUTPUT"
        }
    )

    watercourse_raster = raster_result["OUTPUT"]

    # Calculate Euclidean distance from watercourses
    proximity_result = processing.run(
        "gdal:proximity",
        {
            "INPUT": watercourse_raster,
            "BAND": 1,
            "VALUES": "1",
            "UNITS": 0,
            "MAX_DISTANCE": 0,
            "REPLACE": 0,
            "NODATA": -9999,
            "DATA_TYPE": 5,
            "EXTRA": "",
            "OUTPUT": "TEMPORARY_OUTPUT"
        }
    )

    distance_raster = proximity_result["OUTPUT"]

    # Clip distance raster to study area
    clip_result = processing.run(
        "gdal:cliprasterbymasklayer",
        {
            "INPUT": distance_raster,
            "MASK": bounding_layer,
            "NODATA": -9999,
            "CROP_TO_CUTLINE": False,
            "KEEP_RESOLUTION": True,
            "OUTPUT": str(output_distance)
        }
    )

    clipped_distance = clip_result["OUTPUT"]

    # Define distance suitability classification
    # Range boundaries: min < value <= max
    classification_table = [
        -1, 10, 1,
        10, 20, 2,
        20, 30, 3,
        30, 40, 4,
        40, float("inf"), 5
    ]

    # Reclassify distance raster
    processing.run(
        "native:reclassifybytable",
        {
            "INPUT_RASTER": str(clipped_distance),
            "RASTER_BAND": 1,
            "TABLE": classification_table,
            "NO_DATA": -9999,
            "RANGE_BOUNDARIES": 0,
            "NODATA_FOR_MISSING": True,
            "DATA_TYPE": 5,
            "OUTPUT": str(output_standardised)
        }
    )

    print("Watercourse distance and suitability rasters created")

    return str(output_standardised)

#Existing track rasterize and reclassify function 

# Import required packages
from qgis.core import QgsVectorLayer, QgsRasterLayer
import processing


# Define function for existing track distance suitability
def calculate_track_distance(
    tracks_file,
    bounding_box,
    reference_raster,
    output_distance,
    output_standardised
):
    """
    This function rasterises existing walking tracks, calculates
    Euclidean distance from the tracks, and reclassifies the
    distances into MCDA suitability scores from 1 to 5.

    Parameters
    ----------
    tracks_file : str or Path
        Path to the existing walking tracks vector dataset.

    bounding_box : str or Path
        Path to the study area boundary used for clipping.

    reference_raster : str or Path
        Path to the DEM defining raster extent,
        resolution and pixel alignment.

    output_distance : str or Path
        Path and filename for the Euclidean distance raster.

    output_standardised : str or Path
        Path and filename for the reclassified track
        suitability raster.

    Returns
    -------
    str
        Path to the standardised existing track suitability raster.
    """

    # Load existing walking tracks
    tracks_layer = QgsVectorLayer(
        str(tracks_file),
        "Existing_Tracks",
        "ogr"
    )

    if not tracks_layer.isValid():
        raise ValueError("Existing tracks layer could not be loaded")

    # Load bounding box
    bounding_layer = QgsVectorLayer(
        str(bounding_box),
        "Bounding_Box",
        "ogr"
    )

    if not bounding_layer.isValid():
        raise ValueError("Bounding box could not be loaded")

    # Load reference DEM
    dem_layer = QgsRasterLayer(
        str(reference_raster),
        "DEM"
    )

    if not dem_layer.isValid():
        raise ValueError("Reference DEM could not be loaded")

    # Check coordinate reference systems
    if (
        tracks_layer.crs() != dem_layer.crs()
        or bounding_layer.crs() != dem_layer.crs()
    ):
        raise ValueError(
            "All input datasets must have the same CRS"
        )

    if dem_layer.crs().authid() != "EPSG:7855":
        raise ValueError("Reference DEM must use EPSG:7855")

    if tracks_layer.featureCount() == 0:
        raise ValueError("Existing tracks layer is empty")

    # Rasterise existing walking tracks
    # Track cells = 1, background cells = 0
    raster_result = processing.run(
        "gdal:rasterize",
        {
            "INPUT": tracks_layer,
            "FIELD": None,
            "BURN": 1,
            "UNITS": 0,
            "WIDTH": dem_layer.width(),
            "HEIGHT": dem_layer.height(),
            "EXTENT": dem_layer.extent(),
            "NODATA": None,
            "INIT": 0,
            "DATA_TYPE": 1,
            "EXTRA": "",
            "OUTPUT": "TEMPORARY_OUTPUT"
        }
    )

    tracks_raster = raster_result["OUTPUT"]

    # Calculate Euclidean distance from existing tracks
    proximity_result = processing.run(
        "gdal:proximity",
        {
            "INPUT": tracks_raster,
            "BAND": 1,
            "VALUES": "1",
            "UNITS": 0,
            "MAX_DISTANCE": 0,
            "REPLACE": 0,
            "NODATA": -9999,
            "DATA_TYPE": 5,
            "EXTRA": "",
            "OUTPUT": "TEMPORARY_OUTPUT"
        }
    )

    distance_raster = proximity_result["OUTPUT"]

    # Clip distance raster to the study area
    clip_result = processing.run(
        "gdal:cliprasterbymasklayer",
        {
            "INPUT": distance_raster,
            "MASK": bounding_layer,
            "NODATA": -9999,
            "CROP_TO_CUTLINE": False,
            "KEEP_RESOLUTION": True,
            "OUTPUT": str(output_distance)
        }
    )

    clipped_distance = clip_result["OUTPUT"]

    # Define existing track distance classification
    # RANGE_BOUNDARIES = 0 means min < value <= max
    classification_table = [
        -1, 50, 5,
        50, 100, 4,
        100, 250, 3,
        250, 500, 2,
        500, float("inf"), 1
    ]

    # Reclassify distances into MCDA suitability scores
    processing.run(
        "native:reclassifybytable",
        {
            "INPUT_RASTER": str(clipped_distance),
            "RASTER_BAND": 1,
            "TABLE": classification_table,
            "NO_DATA": -9999,
            "RANGE_BOUNDARIES": 0,
            "NODATA_FOR_MISSING": True,
            "DATA_TYPE": 5,
            "OUTPUT": str(output_standardised)
        }
    )

    print("Existing track distance raster created")
    print("Existing track suitability raster created")

    return str(output_standardised)
