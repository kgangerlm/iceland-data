import sys
from lxml import etree
from pathlib import Path

def parse_kml(file_path):
    """Parse a KML file and return the root element."""
    try:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(file_path, parser)
        return tree
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        sys.exit(1)

def create_new_folder(document, folder_name, namespaces):
    """Create a new folder element with the specified name."""
    folder = etree.SubElement(document, f"{{{namespaces['kml']}}}Folder")
    name = etree.SubElement(folder, f"{{{namespaces['kml']}}}name")
    name.text = folder_name
    return folder

def extract_placemarks(element, namespaces):
    """Recursively extract all Placemark elements from a KML element."""
    placemarks = []
    
    # Get direct placemarks
    for placemark in element.findall(f".//{{{namespaces['kml']}}}Placemark"):
        placemarks.append(placemark)
    
    return placemarks

def merge_kml_files(file_paths, output_path, folder_name):
    """Merge multiple KML files into one with a single folder."""
    if not file_paths:
        print("No input files provided.")
        return

    # Parse the first file to use as base
    base_tree = parse_kml(file_paths[0])
    base_root = base_tree.getroot()
    
    # Define namespaces
    namespaces = {'kml': 'http://www.opengis.net/kml/2.2'}
    
    # Find the Document element in the base KML
    base_document = base_root.find('.//kml:Document', namespaces)
    
    if base_document is None:
        print(f"No Document element found in {file_paths[0]}")
        return
    
    # Create a new folder in the base document
    target_folder = create_new_folder(base_document, folder_name, namespaces)
    
    # Process each file (including the first one)
    for file_path in file_paths:
        print(f"Processing: {file_path}")
        if file_path == file_paths[0]:
            # For the base file
            tree = base_tree
            root = base_root
        else:
            # For additional files
            tree = parse_kml(file_path)
            root = tree.getroot()
        
        # Find Document in the current KML
        document = root.find('.//kml:Document', namespaces)
        if document is None:
            print(f"No Document element found in {file_path}, skipping...")
            continue
        
        # Extract all placemarks from the file (recursively from all folders)
        placemarks = extract_placemarks(document, namespaces)
        
        # Copy each placemark to the target folder
        for placemark in placemarks:
            # Clone the placemark to avoid modification issues
            placemark_copy = etree.fromstring(etree.tostring(placemark))
            target_folder.append(placemark_copy)
            
            # Remove the original placemark if it's from the base file
            if file_path == file_paths[0]:
                placemark.getparent().remove(placemark)
    
    # Remove any empty folders from the base document
    for folder in base_document.findall('.//kml:Folder', namespaces):
        if folder != target_folder and len(folder.findall('./kml:Placemark', namespaces)) == 0:
            # Don't remove folders with subfolders that might have content
            if len(folder.findall('./kml:Folder', namespaces)) == 0:
                folder.getparent().remove(folder)
    
    # Write the merged KML to output file
    base_tree.write(output_path, pretty_print=True, xml_declaration=True, encoding='utf-8')
    print(f"Merged KML written to: {output_path}")

def main():
    """Main function to parse arguments and call merge function."""
    if len(sys.argv) < 4:
        print("Usage: python merge_kml.py output.kml folder_name input1.kml input2.kml [input3.kml ...]")
        sys.exit(1)
    
    output_path = sys.argv[1]
    folder_name = sys.argv[2]
    input_paths = sys.argv[3:]
    
    # Validate input files exist
    for path in input_paths:
        if not Path(path).exists():
            print(f"Input file not found: {path}")
            sys.exit(1)
    
    merge_kml_files(input_paths, output_path, folder_name)

if __name__ == "__main__":
    main()