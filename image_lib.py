'''
Library of useful functions for working with images.
'''
import requests
import sys
import subprocess
import hashlib

from apod_api import APILoader
def main():
    apiLoader = APILoader("2022-06-29")
    apiLoader.get_apod_info()
    image_url = apiLoader.get_apod_image_url()

    imglib = ImageLib(image_url)
    imglib.download_image()
    imglib.save_image("sample.jpg")
  

class ImageLib:
    def __init__(self, image_url):
        self.image_url = image_url
        # self.image_path = image_path


    def download_image(self):
        try:
            response = requests.get(self.image_url)
            self.image_data = response.content
        except Exception as err:
            print(err)
    
    def save_image(self, image_path):
        try:
            with open(image_path, 'wb') as file:
                file.write(self.image_data)
                file.close()
            return True
        except Exception as err:
            print(err)
            return False        
    
    def set_desktop_background_image(image_path):
        try:
            if sys.platform.startswith("win"):
                # Set desktop background image on Windows
                import ctypes
                ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
            elif sys.platform.startswith("darwin"):
                # Set desktop background image on macOS
                script = f'tell application "Finder" to set desktop picture to POSIX file "{image_path}"'
                subprocess.run(['osascript', '-e', script], check=True)
            elif sys.platform.startswith("linux"):
                # Set desktop background image on Linux (requires command-line tool 'feh')
                subprocess.run(['feh', '--bg-fill', image_path], check=True)
            else:
                raise OSError("Unsupported operating system")
            
            return True
        except Exception:
            return False


 
def scale_image(image_size, max_size=(800, 600)):
    """Calculates the dimensions of an image scaled to a maximum width
    and/or height while maintaining the aspect ratio  

    Args:
        image_size (tuple[int, int]): Original image size in pixels (width, height) 
        max_size (tuple[int, int], optional): Maximum image size in pixels (width, height). Defaults to (800, 600).

    Returns:
        tuple[int, int]: Scaled image size in pixels (width, height)
    """
    ## DO NOT CHANGE THIS FUNCTION ##
    # NOTE: This function is only needed to support the APOD viewer GUI
    resize_ratio = min(max_size[0] / image_size[0], max_size[1] / image_size[1])
    new_size = (int(image_size[0] * resize_ratio), int(image_size[1] * resize_ratio))
    return new_size

if __name__ == '__main__':
    main()
