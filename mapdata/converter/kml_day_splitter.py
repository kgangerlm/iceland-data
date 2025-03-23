#!/usr/bin/env python3
"""
KML Region Splitter for Trip Routes
Specialized for Iceland trip data with proper KML namespace handling
"""

import os
import csv
import argparse
import re
import sys
import json
from lxml import etree
from pykml import parser
from shapely.geometry import Point, LineString
from shapely.ops import nearest_points
import geopy.distance
from geopy.geocoders import Nominatim, GoogleV3
import requests
import time

# KML namespace
KML_NS = "{http://www.opengis.net/kml/2.2}"
NS_MAP = {None: "http://www.opengis.net/kml/2.2"}

# Iceland-specific coordinates cache
ICELAND_LOCATIONS = {
    "Norðurfoss, 871, Iceland": (-21.87781, 64.65685),
    "Seljavöllum, Höfn í Hornafirði 781, Iceland": (-15.20629, 64.25162),
    "v/Merkisveg, Borgarfirdi Eystra, 720 Iceland": (-13.81125, 65.51608),
    "Ásgeirsstaðir, Eidar, 701 Iceland": (-14.80988, 65.37715),
    "Departs 4:50 PM GMT": (-21.92893, 64.14554),  # Using Reykjavik coordinates as fallback
}

def parse_tripit_data(csv_file):
    """Parse tripit CSV file and extract lodging locations for each day."""
    lodgings = []
    with open(csv_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Extract day number from "Day X" format
            day_match = re.search(r'\d+', row['Day'])
            day_num = day_match.group(0) if day_match else row['Day']
            
            # Skip entries that don't have a valid day number
            if not day_num.isdigit():
                continue
                
            lodgings.append({
                'day': day_num,
                'date': row['Date'],
                'location': row['Location'],
                'title': row['Title']
            })
    return lodgings

def geocode_location(location_str, api_key=None):
    """Convert a location string to coordinates with fallback to hardcoded values."""
    # Check Iceland-specific locations first
    if location_str in ICELAND_LOCATIONS:
        coords = ICELAND_LOCATIONS[location_str]
        print(f"Using predefined coordinates for '{location_str}': {coords}")
        return coords
    
    # Try Google geocoder if API key provided
    if api_key:
        try:
            geolocator = GoogleV3(api_key=api_key)
            location = geolocator.geocode(location_str)
            if location:
                coords = (location.longitude, location.latitude)
                print(f"Successfully geocoded '{location_str}' to {coords} using Google")
                return coords
            time.sleep(1)  # Respect API rate limits
        except Exception as e:
            print(f"Google geocoding error for '{location_str}': {e}")
    
    # Try Nominatim as fallback
    try:
        geolocator = Nominatim(user_agent="kml_splitter")
        location = geolocator.geocode(location_str)
        if location:
            coords = (location.longitude, location.latitude)
            print(f"Successfully geocoded '{location_str}' to {coords} using Nominatim")
            return coords
        time.sleep(1)  # Respect API rate limits
    except Exception as e:
        print(f"Nominatim geocoding error for '{location_str}': {e}")
    
    # Try with modified string for Iceland addresses (remove postal codes)
    if "Iceland" in location_str:
        try:
            # Remove postal codes (e.g., "720" or "0801")
            simplified = re.sub(r'\b\d{3,4}\b', '', location_str)
            simplified = simplified.replace('  ', ' ').strip()
            
            geolocator = Nominatim(user_agent="kml_splitter")
            location = geolocator.geocode(simplified)
            if location:
                coords = (location.longitude, location.latitude)
                print(f"Successfully geocoded simplified '{simplified}' to {coords}")
                return coords
        except Exception as e:
            print(f"Simplified geocoding error: {e}")
    
    print(f"All geocoding attempts failed for '{location_str}'")
    return None

def get_route_between_locations(start_location, end_location, api_key=None):
    """Get a route between two locations."""
    if not start_location or not end_location:
        return None
    
    # Simple direct route
    return LineString([start_location, end_location])

def distance_point_to_route(point, route):
    """Calculate the minimum distance from a point to a route in miles."""
    if not route:
        return float('inf')
    
    # Convert point to shapely Point
    shapely_point = Point(point)
    
    # Find the nearest point on the route
    nearest_point_on_line = nearest_points(shapely_point, route)[1]
    
    # Calculate distance using geopy
    point_latlon = (point[1], point[0])  # convert to (lat, lon) for geopy
    nearest_latlon = (nearest_point_on_line.y, nearest_point_on_line.x)
    
    distance_miles = geopy.distance.geodesic(point_latlon, nearest_latlon).miles
    
    return distance_miles

def extract_point_from_coordinates(coordinates_str):
    """Extract point coordinates from KML coordinates string."""
    parts = coordinates_str.strip().split(',')
    if len(parts) >= 2:
        try:
            lon = float(parts[0])
            lat = float(parts[1])
            return (lon, lat)
        except ValueError:
            return None
    return None

def is_placemark_near_route(placemark, route, max_distance_miles):
    """Check if a placemark is within the specified distance of the route."""
    try:
        # Find the Point element
        point_elem = placemark.findall('.//' + KML_NS + 'Point')
        if point_elem:
            # Extract coordinates from the Point
            coord_elem = point_elem[0].findall('.//' + KML_NS + 'coordinates')
            if coord_elem and coord_elem[0].text:
                point = extract_point_from_coordinates(coord_elem[0].text)
                if point:
                    distance = distance_point_to_route(point, route)
                    return distance <= max_distance_miles
        
        # For LineString (paths)
        line_elem = placemark.findall('.//' + KML_NS + 'LineString')
        if line_elem:
            coord_elem = line_elem[0].findall('.//' + KML_NS + 'coordinates')
            if coord_elem and coord_elem[0].text:
                # For LineString, we'll check if any point is close enough
                coords_text = coord_elem[0].text.strip().split()
                for coord in coords_text:
                    point = extract_point_from_coordinates(coord)
                    if point:
                        distance = distance_point_to_route(point, route)
                        if distance <= max_distance_miles:
                            return True
    except Exception as e:
        print(f"Error checking placemark proximity: {e}")
    
    return False

def parse_kml_file(kml_file):
    """Parse KML file with pykml."""
    try:
        with open(kml_file, 'rb') as f:
            doc = parser.parse(f)
        return doc.getroot()
    except Exception as e:
        print(f"Error parsing KML file: {e}")
        sys.exit(1)

def filter_placemarks(kml_root, route, max_distance_miles):
    """Find all placemarks in the KML that are within the specified distance of the route."""
    filtered_placemarks = []
    
    # Find all Placemark elements
    try:
        for placemark in kml_root.findall('.//' + KML_NS + 'Placemark'):
            try:
                if is_placemark_near_route(placemark, route, max_distance_miles):
                    # Find the parent of the placemark
                    parent = placemark.getparent()
                    filtered_placemarks.append((placemark, parent))
            except Exception as e:
                # Skip placemarks that cause errors
                print(f"Error processing placemark: {e}")
    except Exception as e:
        print(f"Error finding placemarks: {e}")
    
    return filtered_placemarks

def create_kml_for_day(day, filtered_placemarks, original_kml, output_dir):
    """Create a new KML file for a specific day with filtered placemarks."""
    try:
        # Create a new KML structure with proper namespaces
        kml = etree.Element('kml', nsmap=NS_MAP)
        doc = etree.SubElement(kml, 'Document')
        
        # Set name for the document
        name_elem = etree.SubElement(doc, 'name')
        name_elem.text = f"Day {day} Points of Interest"
        
        # Copy all styles from the original KML
        styles_to_copy = []
        styles_to_copy.extend(original_kml.findall('.//' + KML_NS + 'Style'))
        styles_to_copy.extend(original_kml.findall('.//' + KML_NS + 'StyleMap'))
        
        style_ids = set()
        for style in styles_to_copy:
            style_id = style.get('id', '')
            if style_id not in style_ids:
                style_ids.add(style_id)
                
                # Create a clean copy without namespace prefixes
                style_string = etree.tostring(style).decode('utf-8')
                # Remove namespace declarations and prefixes
                style_string = re.sub(r'xmlns(:ns0)?="[^"]+"', '', style_string)
                style_string = re.sub(r'ns0:', '', style_string)
                
                # Parse back to XML and add to the document
                try:
                    clean_style = etree.fromstring(style_string)
                    doc.append(clean_style)
                except Exception as e:
                    print(f"Error cleaning style {style_id}: {e}")
        
        # Group placemarks by folder
        placemarks_by_folder = {}
        for placemark, parent in filtered_placemarks:
            folder_name = "Points of Interest"
            if parent.tag == KML_NS + 'Folder':
                name_elem = parent.find('./' + KML_NS + 'name')
                if name_elem is not None and name_elem.text:
                    folder_name = name_elem.text
            
            if folder_name not in placemarks_by_folder:
                placemarks_by_folder[folder_name] = []
            
            placemarks_by_folder[folder_name].append(placemark)
        
        # Create folders and add placemarks
        for folder_name, placemarks in placemarks_by_folder.items():
            folder = etree.SubElement(doc, 'Folder')
            folder_name_elem = etree.SubElement(folder, 'name')
            folder_name_elem.text = folder_name
            
            for placemark in placemarks:
                # Create a clean copy of the placemark without namespace prefixes
                placemark_string = etree.tostring(placemark).decode('utf-8')
                # Remove namespace declarations and prefixes
                placemark_string = re.sub(r'xmlns(:ns0)?="[^"]+"', '', placemark_string)
                placemark_string = re.sub(r'ns0:', '', placemark_string)
                
                try:
                    clean_placemark = etree.fromstring(placemark_string)
                    folder.append(clean_placemark)
                except Exception as e:
                    print(f"Error adding placemark to folder: {e}")
        
        # Write the KML file
        output_file = os.path.join(output_dir, f'day-{day}.kml')
        with open(output_file, 'wb') as f:
            # Write a clean XML declaration and KML root
            f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write(etree.tostring(kml, pretty_print=True))
        
        # Validate the file
        try:
            with open(output_file, 'rb') as f:
                parser.parse(f)
            print(f"Successfully created valid KML file for Day {day} with {len(filtered_placemarks)} placemarks")
            return True
        except Exception as e:
            print(f"Warning: Created KML file for Day {day} but validation failed: {e}")
            return True  # Still return True since we created the file
            
    except Exception as e:
        print(f"Error creating KML file for Day {day}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Split KML file into different regions based on trip data.')
    parser.add_argument('kml_file', help='Input KML file')
    parser.add_argument('tripit_file', help='Trip data CSV file')
    parser.add_argument('output_dir', help='Directory to output split KML files')
    parser.add_argument('--radius', type=float, default=30, help='Radius in miles to consider points around the route (default: 30)')
    parser.add_argument('--api-key', help='Google Maps API key for geocoding')
    parser.add_argument('--all-days', action='store_true', help='Create KML files for all days, even without routes')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    # Parse KML file - do this first to ensure it's valid before geocoding
    print(f"Parsing KML file: {args.kml_file}")
    kml_root = parse_kml_file(args.kml_file)
    
    # Parse trip data
    print(f"Parsing trip data from: {args.tripit_file}")
    lodgings = parse_tripit_data(args.tripit_file)
    
    # Geocode all locations first
    print("Geocoding all locations...")
    for lodging in lodgings:
        lodging['coordinates'] = geocode_location(lodging['location'], args.api_key)
        time.sleep(0.5)  # Respect API rate limits
    
    # Process each pair of consecutive days
    processed_days = set()
    
    for i in range(len(lodgings) - 1):
        current_day = lodgings[i]['day']
        next_day = lodgings[i + 1]['day']
        current_loc = lodgings[i]['location']
        next_loc = lodgings[i + 1]['location']
        
        print(f"\nProcessing route from Day {current_day} ({current_loc}) to Day {next_day} ({next_loc})")
        
        # Skip if either location doesn't have coordinates
        if not lodgings[i].get('coordinates') or not lodgings[i + 1].get('coordinates'):
            print(f"  Skipping: missing coordinates for one or both locations")
            continue
        
        # Create route
        route = get_route_between_locations(
            lodgings[i]['coordinates'], 
            lodgings[i + 1]['coordinates'],
            args.api_key
        )
        
        if not route:
            print(f"  Skipping: couldn't create route")
            continue
        
        # Filter placemarks by distance to route
        print(f"  Finding points within {args.radius} miles of route...")
        filtered_placemarks = filter_placemarks(kml_root, route, args.radius)
        
        # Create KML file for the next day's points
        print(f"  Creating KML file for Day {next_day} with {len(filtered_placemarks)} placemarks")
        success = create_kml_for_day(next_day, filtered_placemarks, kml_root, args.output_dir)
        
        if success:
            processed_days.add(next_day)
    
    # Process the first day if it wasn't already (since it won't be a "next day" in any pair)
    if lodgings and '1' not in processed_days:
        if lodgings[0]['coordinates']:
            # For the first day, create a small radius around the first hotel
            print(f"\nProcessing first day location: {lodgings[0]['location']}")
            center_point = lodgings[0]['coordinates']
            
            # Create a tiny "route" (just the point itself and a point 1 mile away)
            # This lets us reuse the same filtering logic
            offset_point = (center_point[0] + 0.01, center_point[1] + 0.01)  # Roughly 1 mile
            tiny_route = LineString([center_point, offset_point])
            
            # Use a larger radius for just the first day's location
            first_day_radius = args.radius * 2
            print(f"  Finding points within {first_day_radius} miles of first lodging...")
            filtered_placemarks = filter_placemarks(kml_root, tiny_route, first_day_radius)
            
            print(f"  Creating KML file for Day 1 with {len(filtered_placemarks)} placemarks")
            success = create_kml_for_day('1', filtered_placemarks, kml_root, args.output_dir)
            
            if success:
                processed_days.add('1')
    
    # If requested, create files for all days, copying from adjacent days if needed
    if args.all_days:
        print("\nCreating KML files for any missing days...")
        for lodging in lodgings:
            day = lodging['day']
            if day not in processed_days:
                # Find the nearest processed day
                nearest_day = None
                nearest_distance = float('inf')
                
                for processed_day in processed_days:
                    distance = abs(int(day) - int(processed_day))
                    if distance < nearest_distance:
                        nearest_distance = distance
                        nearest_day = processed_day
                
                if nearest_day:
                    print(f"  Day {day} not processed. Copying from Day {nearest_day}...")
                    # Copy the KML file
                    src_file = os.path.join(args.output_dir, f'day-{nearest_day}.kml')
                    dst_file = os.path.join(args.output_dir, f'day-{day}.kml')
                    
                    if os.path.exists(src_file):
                        try:
                            with open(src_file, 'r', encoding='utf-8') as src:
                                content = src.read()
                                
                                # Replace the name in the KML content
                                content = content.replace(
                                    f'Day {nearest_day} Points of Interest', 
                                    f'Day {day} Points of Interest'
                                )
                                
                                with open(dst_file, 'w', encoding='utf-8') as dst:
                                    dst.write(content)
                                
                                processed_days.add(day)
                        except Exception as e:
                            print(f"    Error copying KML file: {e}")
    
    # Print summary
    print("\nSummary:")
    print(f"Successfully created KML files for {len(processed_days)} days")
    print(f"Days processed: {', '.join(sorted(processed_days, key=int))}")
    
    missing_days = set(lodging['day'] for lodging in lodgings) - processed_days
    if missing_days:
        print(f"Days not processed: {', '.join(sorted(missing_days, key=int))}")
        print("Try using the --all-days flag to create files for all days")
    
    print(f"\nFiles saved in {args.output_dir}")

if __name__ == "__main__":
    main()