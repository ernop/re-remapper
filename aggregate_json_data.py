import json, traceback
import os
import datetime
import json_repair

def parse_housing_data(json_file):
    try:
        with open(json_file, 'r') as file:
            content = file.read()
        
        # Repair the JSON using json_repair
        repaired_content = json_repair.repair_json(content)
        
        # Parse the repaired JSON
        data = json.loads(repaired_content)
        
        # Extract the list of search results
        resultGroups = [data.get('cat1', {}).get('searchResults', {}).get('listResults', []), 
                        data.get('cat1', {}).get('searchResults', {}).get('mapResults', [])]
        
        zpids = set()
        parsed_data = []
        for results in resultGroups:
            for home in results:
                home_info = home.get('hdpData', {}).get('homeInfo', {})
                
                # Extract latitude and longitude
                latitude = home.get('latLong', {}).get('latitude') or home_info.get('latitude')
                longitude = home.get('latLong', {}).get('longitude') or home_info.get('longitude')
                
                # Skip if latitude or longitude is invalid
                if not latitude or not longitude or not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
                    print('skip invalid geocode.')
                    continue

                parsed_home = {
                    'zpid': int(home.get('zpid') or home_info.get('zpid') or 0),
                    'latitude': float(latitude),
                    'longitude': float(longitude),
                    'price': float(home.get('unformattedPrice') or home_info.get('price') or home.get('price') or 0),
                    'address': str(home.get('address') or home.get('streetAddress') or home_info.get('streetAddress') or ''),
                    'city': str(home.get('addressCity') or home.get('city') or home_info.get('city') or ''),
                    'state': str(home.get('addressState') or home.get('state') or home_info.get('state') or ''),
                    'zipcode': str(home.get('addressZipcode') or home.get('zipcode') or home_info.get('zipcode') or ''),
                    'bedrooms': float(home.get('beds') or home_info.get('bedrooms') or 0),
                    'bathrooms': float(home.get('baths') or home_info.get('bathrooms') or 0),
                    'living_area': float(home.get('area') or home_info.get('livingArea') or 0),
                    'lot_area_value': float(home_info.get('lotAreaValue') or 0),
                    'lot_area_unit': str(home_info.get('lotAreaUnit') or ''),
                    'sale_date': int(home.get('dateSold') or home_info.get('dateSold') or 0),
                    'zestimate': float(home.get('zestimate') or home_info.get('zestimate') or 0),
                    'rent_zestimate': float(home.get('rentZestimate') or home_info.get('rentZestimate') or 0),
                    'home_type': str(home.get('homeType') or home_info.get('homeType') or ''),
                }
                
                if parsed_home['zpid'] in zpids:
                    print("skipping dupzpid.")
                    continue
                
                zpids.add(parsed_home['zpid'])
                # Only add homes with valid latitude, longitude, and price
                if parsed_home['latitude'] and parsed_home['longitude'] and parsed_home['price']:
                    parsed_data.append(parsed_home)
                else:
                    print("skipping missing geocode or missing price.")
        
        return parsed_data
    except Exception as e:
        print(f"Error processing {json_file}: {str(e)}.")
        print(f"Error type: {type(e).__name__}")
        print(f"Error details: {e.args}")
        print(f"Traceback: {traceback.format_exc()}")
        return []

def display_price(price):
    return f"{int(price // 1000)}k"

def aggregate_json_data(folder):
    all_data = []
    total_houses = 0
    source_files = []

    for filename in os.listdir(folder):
        if filename.endswith('.json'):
            file_path = os.path.join(folder, filename)
            parsed_data = parse_housing_data(file_path)
            if parsed_data:
                all_data.extend(parsed_data)
                num_houses = len(parsed_data)
                total_houses += num_houses
                source_files.append(filename)
                print(f"File: {filename}, Houses found: {num_houses}")
            else:
                print(f"File: {filename}, No valid data found")

    print(f"Total houses found across all files: {total_houses}")

    # Create the unified JSON structure
    unified_data = {
        "houses": all_data,
        "metadata": {
            "total_houses": total_houses,
            "source_files": source_files
        }
    }

    # Generate the output filename with date and hour
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H")
    output_filename = f"{os.path.basename(folder)}_{total_houses}_houses_{current_datetime}.json"
    output_path = os.path.join(folder, output_filename)

    # Save the unified JSON data
    with open(output_path, 'w') as outfile:
        json.dump(unified_data, outfile, indent=2)

    print(f"Unified housing data saved as {output_filename}")

    # we do NOT call make_map. We just prepare the data.

def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python aggregate_json_data.py <folder>")
        folder='data-pa'
    else:
        folder = sys.argv[1]
    if not os.path.isdir(folder):
        print(f"Error: {folder} is not a valid directory")
        sys.exit(1)

    aggregate_json_data(folder)

if __name__ == "__main__":
    main()