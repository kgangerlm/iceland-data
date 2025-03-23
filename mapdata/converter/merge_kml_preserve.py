import sys
from lxml import etree
from pathlib import Path
import copy

def parse_kml(file_path):
    """Parse a KML file and return the root element."""
    try:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(file_path, parser)
        return tree
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        sys.exit(1)

def get_folder_name(folder, namespaces):
    """Get the name of a folder element."""
    name_elem = folder.find(f".//{{{namespaces['kml']}}}name")
    if name_elem is not None and name_elem.text:
        return name_elem.text
    return "Unnamed Folder"

def find_or_create_folder(parent, folder_name, namespaces):
    """Find a folder with the given name or create a new one."""
    for folder in parent.findall(f".//{{{namespaces['kml']}}}Folder"):
        name = get_folder_name(folder, namespaces)
        if name == folder_name:
            return folder
    
    # Folder not found, create a new one
    new_folder = etree.SubElement(parent, f"{{{namespaces['kml']}}}Folder")
    name_elem = etree.SubElement(new_folder, f"{{{namespaces['kml']}}}name")
    name_elem.text = folder_name
    return new_folder

def merge_folders(base_document, folder, namespaces):
    """Recursively merge a folder and its contents into the base document."""
    folder_name = get_folder_name(folder, namespaces)
    
    # Find or create matching folder in base document
    target_folder = find_or_create_folder(base_document, folder_name, namespaces)
    
    # Copy all placemarks to the target folder
    for placemark in folder.findall(f".//{{{namespaces['kml']}}}Placemark"):
        if placemark.getparent() == folder:  # Only direct children
            placemark_copy = copy.deepcopy(placemark)
            target_folder.append(placemark_copy)
    
    # Recursively process subfolders
    for subfolder in folder.findall(f".//{{{namespaces['kml']}}}Folder"):
        if subfolder.getparent() == folder:  # Only direct children
            merge_folders(target_folder, subfolder, namespaces)

def merge_kml_files(file_paths, output_path):
    """Merge multiple KML files while preserving folder structure."""
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
    
    # Process each additional file
    for file_path in file_paths[1:]:
        print(f"Merging: {file_path}")
        tree = parse_kml(file_path)
        root = tree.getroot()
        
        # Find Document in the current KML
        document = root.find('.//kml:Document', namespaces)
        if document is None:
            print(f"No Document element found in {file_path}, skipping...")
            continue
        
        # Process top-level folders
        for folder in document.findall(f".//{{{namespaces['kml']}}}Folder"):
            if folder.getparent() == document:  # Only top-level folders
                merge_folders(base_document, folder, namespaces)
        
        # Process top-level placemarks (not in folders)
        for placemark in document.findall(f".//{{{namespaces['kml']}}}Placemark"):
            if placemark.getparent() == document:  # Only top-level placemarks
                placemark_copy = copy.deepcopy(placemark)
                base_document.append(placemark_copy)
    
    # Write the merged KML to output file
    base_tree.write(output_path, pretty_print=True, xml_declaration=True, encoding='utf-8')
    print(f"Merged KML written to: {output_path}")

def main():
    """Main function to parse arguments and call merge function."""
    if len(sys.argv) < 3:
        print("Usage: python merge_kml_preserve.py output.kml input1.kml input2.kml [input3.kml ...]")
        sys.exit(1)
    
    output_path = sys.argv[1]
    input_paths = sys.argv[2:]
    
    # Validate input files exist
    for path in input_paths:
        if not Path(path).exists():
            print(f"Input file not found: {path}")
            sys.exit(1)
    
    merge_kml_files(input_paths, output_path)

if __name__ == "__main__":
    main()