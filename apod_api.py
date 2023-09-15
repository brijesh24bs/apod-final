import requests
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

class APILoader:
    def __init__(self, apod_date):
        self.apod_date = apod_date
        self.API_KEY  = os.environ.get('API_KEY')

    def get_apod_info(self):
        url = f"https://api.nasa.gov/planetary/apod?date={self.apod_date}&api_key={self.API_KEY}"
        response = requests.get(url)

        if response.ok:
            self.apod_info_dict = response.json()   
        else:
            self.apod_info_dict =  None

        return self.apod_info_dict

    def get_apod_image_url(self):
        media_type = self.apod_info_dict.get("media_type")
        if media_type == "image":
            return self.apod_info_dict.get("hdurl")
        elif media_type == "video":
            return self.apod_info_dict.get("thumbnail_url")
        else:
            return None
    
    def get_sha256(self):
        input_string = self.apod_info_dict['date'] + self.apod_info_dict['explanation'] + self.apod_info_dict['title']
        sha256 = hashlib.sha256()
        sha256.update(input_string.encode('utf-8'))
        return sha256.hexdigest()
        
        

# def main():
#     # Testing the functions
#     apod_date = "2023-06-29"  # Example APOD date
#     apod_info = get_apod_info(apod_date)
#     if apod_info:
#         apod_image_url = get_apod_image_url(apod_info)
#         print("APOD Image URL:", apod_image_url)
#     else:
#         print("Failed to retrieve APOD information.")

if __name__ == '__main__':
    apiLoader = APILoader("2023-06-29")
    apod_info = apiLoader.get_apod_info()
    print(apiLoader.get_sha256())