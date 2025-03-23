# KML Splitter for Trip Routes

## Overview

This script splits a KML file into separate files for each day of your trip based on proximity to your daily routes.

## Installation

### Required Libraries

You'll need to install the following Python libraries:

```bash
pip install lxml pykml shapely geopy requests
```

## Usage

Save the script as `kml_splitter.py` and run it from the command line:

```bash
python kml_splitter.py your_places.kml tripit_data.csv output_folder
```

### Parameters

- `your_places.kml`: Your input KML file containing points of interest
- `tripit_data.csv`: CSV file with your lodging information
- `output_folder`: Directory where the daily KML files will be saved

### Example

```bash
python kml_splitter.py vacation_poi.kml tripit_data.csv daily_routes
```

### Optional Parameters

You can also adjust the search radius:

```bash
python kml_splitter.py vacation_poi.kml tripit_data.csv daily_routes --radius 40
```

If you have a Google Maps API key for more accurate routing:

```bash
python kml_splitter.py vacation_poi.kml tripit_data.csv daily_routes --api-key YOUR_API_KEY
```

## Output

The script will create files named `day-1.kml`, `day-2.kml`, etc. in your output folder, each containing only the points relevant to that day's journey.

## How It Works

1. Reads your lodging information from the CSV file
2. Geocodes each location to get coordinates
3. Creates routes between consecutive lodging locations
4. Filters points from your KML file based on their proximity to each day's route
5. Preserves all original KML styling, including icons and other metadata
6. Creates a separate KML file for each day of your trip
