import csv
import requests
import time
from tqdm import tqdm
import pandas as pd
def get_street_from_point(point):
    """
    Takes a POINT string (e.g., 'POINT (7.619825467000055 45.03701834200007)')
    and returns the street name by querying the OpenStreetMap Nominatim API.
    """
    # Extract longitude and latitude from the POINT string
    coords = point.replace("POINT (", "").replace(")", "").split()
    lon, lat = coords[0], coords[1]

    # Query OpenStreetMap Nominatim API
    url = f"https://nominatim.openstreetmap.org/reverse"
    params = {
        'format': 'json',
        'lat': lat,
        'lon': lon,
        'addressdetails': 1
    }
    headers = {
    'User-Agent': 'myapp/1.0 (marco.stranisci@aqua-tech.com)'  # Replace with your app name and email
}

    response = requests.get(url, params=params,headers=headers)
    time.sleep(1)  # To avoid hitting the API too fast

    

    if response.status_code == 200:
        data = response.json()
        return data.get('address', {}).get('road', 'Street not found'),data.get('address', {}).get('suburb', 'Suburb not found')
    else:
        return 'Error querying OpenStreetMap API'

def process_csv_and_get_streets(csv_file_path, output_file_path):
    """
    Reads a CSV file containing POINT data, applies the get_street_from_point function,
    and saves the results to an output file.
    """
    with open(csv_file_path, mode='r') as file:
        reader = pd.read_csv(file)
        reader = reader.drop_duplicates(subset=['centroid'])
        

        with open(output_file_path, mode='w', newline='') as output_file:
            writer = csv.writer(output_file)
            writer.writerow(['centroid', 'Street','Suburb'])  # Write header to the output file

            for _,row in tqdm(reader.iterrows(),total=len(reader)):
                
                point = row.centroid # Assuming the POINT data is in the first column
                street,suburb = get_street_from_point(point)
                writer.writerow([point, street,suburb])

# Example usage
csv_file_path = '/Users/marco/Documents/unito/nudging-ontology/data/f1_census.csv'
output_file_path = '/Users/marco/Documents/unito/nudging-ontology/data/f1_census_with_streets.csv'
process_csv_and_get_streets(csv_file_path, output_file_path)
process_csv_and_get_streets(csv_file_path)