import csv
import os
from xml.dom import minidom

def create_kml_from_csv(csv_file_path, output_folder):
    """
    Convert a CSV file to multiple KML files, one for each day.
    
    Args:
        csv_file_path (str): Path to the CSV file
        output_folder (str): Folder to save the KML files
    """
    # Read CSV file
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
        
        print(f"Read {len(rows)} rows from {csv_file_path}")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return
    
    # Group rows by day
    days = {}
    for i, row in enumerate(rows):
        day = row.get('Day', '').strip()
        if not day:  # Skip rows without day value
            print(f"Warning: Row {i+2} has no Day value, skipping.")
            continue
        
        if day not in days:
            days[day] = []
        days[day].append(row)
    
    print(f"Found {len(days)} different days")
    
    # Create KML for each day
    for day, day_rows in days.items():
        try:
            # Create KML document
            doc = minidom.Document()
            
            # Create KML root element
            kml = doc.createElement('kml')
            kml.setAttribute('xmlns', 'http://www.opengis.net/kml/2.2')
            doc.appendChild(kml)
            
            # Create Document element
            document = doc.createElement('Document')
            kml.appendChild(document)
            
            # Create Folder for the day
            folder = doc.createElement('Folder')
            document.appendChild(folder)
            
            # Add name to folder
            name = doc.createElement('name')
            name_text = doc.createTextNode(day)
            name.appendChild(name_text)
            folder.appendChild(name)
            
            # Create style map for icons
            # We'll create a style for each unique icon
            icon_styles = {}
            placemark_count = 0
            
            # Add placemarks for each row
            for i, row in enumerate(day_rows):
                # Skip rows without title, coordinates, or description
                if not row.get('Title'):
                    print(f"Warning: Row for {day} has no Title, skipping.")
                    continue
                if not row.get('Coordinates'):
                    print(f"Warning: Row for {day}, '{row.get('Title')}' has no Coordinates, skipping.")
                    continue
                    
                # Create style for icon if not already created
                icon_url = row.get('Icon', 'http://maps.google.com/mapfiles/kml/shapes/info.png')
                if icon_url not in icon_styles:
                    style_id = f"style_{len(icon_styles)}"
                    
                    style = doc.createElement('Style')
                    style.setAttribute('id', style_id)
                    
                    icon_style = doc.createElement('IconStyle')
                    icon = doc.createElement('Icon')
                    href = doc.createElement('href')
                    href_text = doc.createTextNode(icon_url)
                    
                    href.appendChild(href_text)
                    icon.appendChild(href)
                    icon_style.appendChild(icon)
                    style.appendChild(icon_style)
                    
                    document.appendChild(style)
                    icon_styles[icon_url] = style_id
                else:
                    style_id = icon_styles[icon_url]
                
                # Create placemark
                placemark = doc.createElement('Placemark')
                
                # Add name
                pm_name = doc.createElement('name')
                pm_name_text = doc.createTextNode(row['Title'])
                pm_name.appendChild(pm_name_text)
                placemark.appendChild(pm_name)
                
                # Add description
                if row.get('Description'):
                    description = doc.createElement('description')
                    cdata = doc.createCDATASection(row['Description'])
                    description.appendChild(cdata)
                    placemark.appendChild(description)
                
                # Add style reference
                style_url = doc.createElement('styleUrl')
                style_url_text = doc.createTextNode(f"#{style_id}")
                style_url.appendChild(style_url_text)
                placemark.appendChild(style_url)
                
                # Add point
                point = doc.createElement('Point')
                coordinates = doc.createElement('coordinates')
                
                # Parse lat,lng from Coordinates column
                coord_text = row['Coordinates']
                try:
                    # KML expects: longitude,latitude,altitude
                    # Our format is: latitude,longitude
                    lat, lng = coord_text.split(',')
                    kml_coords = f"{lng},{lat},0"  # Adding 0 for altitude
                    
                    coord_text_node = doc.createTextNode(kml_coords)
                    coordinates.appendChild(coord_text_node)
                    point.appendChild(coordinates)
                    placemark.appendChild(point)
                    
                    # Add to folder
                    folder.appendChild(placemark)
                    placemark_count += 1
                except Exception as e:
                    print(f"Error processing coordinates for {row['Title']}: {e}")
            
            # Write KML to file
            day_filename = day.replace(' ', '_').lower()
            output_file_path = os.path.join(output_folder, f"{day_filename}.kml")
            
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(doc.toprettyxml(indent='  '))
            
            print(f"Created KML file for {day}: {output_file_path} with {placemark_count} placemarks")
        except Exception as e:
            print(f"Error creating KML for {day}: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python csv_to_kml.py <csv_file_path> <output_folder>")
        sys.exit(1)
    
    csv_file_path = sys.argv[1]
    output_folder = sys.argv[2]
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    create_kml_from_csv(csv_file_path, output_folder)
