# Iceland Itinerary CSV to KML Converter

This project contains:
1. An enhanced CSV file with Iceland itinerary data
2. A Python script to convert the CSV file into daily KML files

## Enhanced CSV File

The `iceland_enhanced.csv` file includes:
- Standardized activity types
- Rich HTML descriptions with emojis
- KML icon URLs for each activity
- Accurate geographic coordinates for all locations

## CSV to KML Converter

### Requirements
- Python 3.6 or higher
- CSV file with the following columns:
  - Day: The day of the itinerary (e.g., "Day 1", "Day 2")
  - Title: The name of the place or activity
  - Description: Rich HTML description of the place
  - Coordinates: Geographic coordinates in format "latitude,longitude"
  - Icon: URL to a KML-compatible icon

### Usage

```bash
python csv_to_kml.py <csv_file_path> <output_folder>
```

Example:
```bash
python csv_to_kml.py iceland_enhanced.csv kml_files
```

This will read the CSV file and create a separate KML file for each day in your itinerary.

### Output

The script will:
- Create one KML file for each day in the itinerary
- Name files based on the day (e.g., `day_1.kml`, `day_2.kml`)
- Each KML file contains one folder with the name format "Day [number]"
- Include all places and activities for that day as placemarks
- Apply appropriate icons based on activity type
- Include rich HTML descriptions in each placemark

### Important Notes

- The script converts coordinates from "latitude,longitude" (CSV) to "longitude,latitude,0" (KML format)
- Rows without a Day, Title, or Coordinates value will be skipped
- You can update the CSV file and re-run the script to regenerate the KML files
- The script handles special characters and HTML content in descriptions

### Customization

If you need to customize the KML output:
- Edit the script to add additional styling elements
- Modify the icon URLs in the CSV file
- Update coordinates or descriptions as needed in the CSV
