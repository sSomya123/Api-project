import requests
from geopy.geocoders import Nominatim

def get_location(city_name):
    geolocator = Nominatim(user_agent="pin_code_locator")
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    else:
        print("City not found!")
        return None, None

def get_pin_code(city_name, username):
    latitude, longitude = get_location(city_name)
    if latitude is None or longitude is None:
        return None

    # GeoNames API URL to search for postal codes
    geonames_url = f"http://api.geonames.org/postalCodeSearchJSON?placename={city_name}&username={username}"
    print("Requesting:", geonames_url)  # Debugging line to check the API URL
    
    response = requests.get(geonames_url)
    
    print("Response Status Code:", response.status_code)  # Debugging line to check the response code
    
    if response.status_code == 200:
        data = response.json()
        if "postalCodes" in data and len(data["postalCodes"]) > 0:
            postal_code = data["postalCodes"][0]["postalCode"]
            return postal_code
        else:
            print("Postal code not found.")
            return None
    else:
        print("Error fetching data from GeoNames. Status code:", response.status_code)
        print("Response Content:", response.text)  # Show response content to help debug
        return None

def main():
    city_name = input("Enter the city or town name: ")
    username = input("Enter your GeoNames username (API key): ")  # Get this from GeoNames website
    pin_code = get_pin_code(city_name, username)
    
    if pin_code:
        print(f"The pin code for {city_name} is: {pin_code}")
    else:
        print("Unable to fetch the pin code.")

if __name__ == "__main__":
    main()
