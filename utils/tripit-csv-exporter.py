#!/usr/bin/env python3
import csv
import argparse
import requests
import datetime
import base64
import xml.etree.ElementTree as ET
from datetime import timedelta

def main():
    # Set up command line arguments
    parser = argparse.ArgumentParser(description='Export TripIt booking data to CSV')
    parser.add_argument('--username', required=True, help='TripIt username/email')
    parser.add_argument('--password', required=True, help='TripIt password')
    parser.add_argument('--trip-id', help='Specific trip ID to export (optional)')
    parser.add_argument('--output', default='tripit_bookings.csv', help='Output CSV filename')
    args = parser.parse_args()
    
    # Set up Basic Authentication
    auth_str = f"{args.username}:{args.password}"
    auth_bytes = auth_str.encode('ascii')
    base64_auth = base64.b64encode(auth_bytes).decode('ascii')
    headers = {
        'Authorization': f'Basic {base64_auth}',
        'Accept': 'application/xml'
    }
    
    api_url = 'https://api.tripit.com/v1'
    
    # Prepare CSV file
    with open(args.output, 'w', newline='') as csvfile:
        fieldnames = ['day_number', 'date', 'title', 'category', 'total_cost', 'booking_site']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Get trips
        if args.trip_id:
            # Get single trip
            response = requests.get(f"{api_url}/get/trip/id/{args.trip_id}", headers=headers)
            if response.status_code != 200:
                print(f"Error fetching trip: {response.status_code}")
                return
            
            # Parse XML response
            root = ET.fromstring(response.content)
            trips = [process_trip_xml(root.find('.//Trip'))]
        else:
            # Get all trips
            response = requests.get(f"{api_url}/list/trip", headers=headers)
            if response.status_code != 200:
                print(f"Error fetching trips: {response.status_code}")
                return
            
            # Parse XML response
            root = ET.fromstring(response.content)
            trips = [process_trip_xml(trip) for trip in root.findall('.//Trip')]
        
        for trip in trips:
            if not trip:
                continue
                
            trip_id = trip.get('id')
            try:
                trip_start = datetime.datetime.strptime(trip.get('start_date'), '%Y-%m-%d')
                trip_end = datetime.datetime.strptime(trip.get('end_date'), '%Y-%m-%d')
            except (ValueError, TypeError):
                print(f"Invalid date format in trip {trip_id}")
                continue
            
            # Get detailed trip info if not already fetched
            if args.trip_id:
                trip_detail = trip
            else:
                response = requests.get(f"{api_url}/get/trip/id/{trip_id}", headers=headers)
                if response.status_code != 200:
                    print(f"Error fetching trip details: {response.status_code}")
                    continue
                
                root = ET.fromstring(response.content)
                trip_detail = process_trip_xml(root.find('.//Trip'))
            
            # Process bookings from trip data
            bookings = []
            
            # Process lodging
            for lodging in trip_detail.get('lodging', []):
                try:
                    check_in = datetime.datetime.strptime(lodging.get('start_date'), '%Y-%m-%d')
                    check_out = datetime.datetime.strptime(lodging.get('end_date'), '%Y-%m-%d')
                except (ValueError, TypeError):
                    continue
                
                # Add entry for each day of stay (excluding checkout)
                current_date = check_in
                while current_date < check_out:
                    bookings.append({
                        'date': current_date.strftime('%Y-%m-%d'),
                        'title': lodging.get('name', 'Lodging'),
                        'category': 'lodging',
                        'total_cost': lodging.get('total_cost', ''),
                        'booking_site': lodging.get('booking_site', '')
                    })
                    current_date += timedelta(days=1)
            
            # Process car rentals
            for car in trip_detail.get('car', []):
                try:
                    pickup_date = datetime.datetime.strptime(car.get('start_date'), '%Y-%m-%d')
                except (ValueError, TypeError):
                    continue
                
                bookings.append({
                    'date': pickup_date.strftime('%Y-%m-%d'),
                    'title': f"{car.get('car_type', '')} - {car.get('company', '')}",
                    'category': 'rental car',
                    'total_cost': car.get('total_cost', ''),
                    'booking_site': car.get('booking_site', '')
                })
            
            # Process activities
            for activity in trip_detail.get('activity', []):
                try:
                    activity_date = datetime.datetime.strptime(activity.get('start_date'), '%Y-%m-%d')
                except (ValueError, TypeError):
                    continue
                
                bookings.append({
                    'date': activity_date.strftime('%Y-%m-%d'),
                    'title': activity.get('display_name', 'Activity'),
                    'category': 'activity',
                    'total_cost': activity.get('total_cost', ''),
                    'booking_site': activity.get('booking_site', '')
                })
            
            # Sort bookings by date
            bookings.sort(key=lambda x: x['date'])
            
            # Add day number and write to CSV
            for booking in bookings:
                booking_date = datetime.datetime.strptime(booking['date'], '%Y-%m-%d')
                days_from_start = (booking_date - trip_start).days + 1
                booking['day_number'] = days_from_start
                writer.writerow(booking)

def process_trip_xml(trip_elem):
    """Process Trip XML element into a dictionary"""
    if trip_elem is None:
        return None
        
    trip_dict = {
        'id': trip_elem.findtext('id'),
        'name': trip_elem.findtext('display_name'),
        'start_date': trip_elem.findtext('start_date'),
        'end_date': trip_elem.findtext('end_date'),
        'lodging': [],
        'car': [],
        'activity': []
    }
    
    # Process lodging
    for lodging in trip_elem.findall('.//LodgingObject'):
        lodging_dict = {
            'name': lodging.findtext('display_name'),
            'start_date': lodging.findtext('StartDateTime/date'),
            'end_date': lodging.findtext('EndDateTime/date'),
            'booking_site': lodging.findtext('booking_site_name'),
            'total_cost': lodging.findtext('total_cost/amount')
        }
        trip_dict['lodging'].append(lodging_dict)
    
    # Process car rentals
    for car in trip_elem.findall('.//CarObject'):
        car_dict = {
            'company': car.findtext('vendor'),
            'car_type': car.findtext('vehicle_type'),
            'start_date': car.findtext('StartDateTime/date'),
            'end_date': car.findtext('EndDateTime/date'),
            'booking_site': car.findtext('booking_site_name'),
            'total_cost': car.findtext('total_cost/amount')
        }
        trip_dict['car'].append(car_dict)
    
    # Process activities
    for activity in trip_elem.findall('.//ActivityObject'):
        activity_dict = {
            'display_name': activity.findtext('display_name'),
            'start_date': activity.findtext('StartDateTime/date'),
            'booking_site': activity.findtext('booking_site_name'),
            'total_cost': activity.findtext('total_cost/amount')
        }
        trip_dict['activity'].append(activity_dict)
    
    return trip_dict

if __name__ == "__main__":
    main()
