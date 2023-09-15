from datetime import datetime
from datetime import date
import os
import inspect
import sys

import sqlite3
from image_lib import ImageLib
from apod_api import APILoader


# def main():
#     ## DO NOT CHANGE THIS FUNCTION ##
#     # Get the APOD date from the command line
#     apod_date = get_apod_date()

#     # Get the path of the directory in which this script resides
#     script_dir = get_script_dir()

#     # Initialize the image cache
#     init_apod_cache(script_dir)

#     # Add the APOD for the specified date to the cache
#     apod_id = add_apod_to_cache(apod_date)

#     # Get the information for the APOD from the DB
#     apod_info = get_apod_info(apod_id)

#     # Set the APOD as the desktop background image
#     if apod_id != 0:
#         image_lib.set_desktop_background_image(apod_info['file_path'])

class APOD:
    def __init__(self) -> None:
        self.image_cache_dir = None  # Full path of image cache directory
        self.image_cache_db = None   # Full path of image cache database
        self.apod_date = None        # Date of APOD to download

    def get_apod_date(self):
        try:
            if len(sys.argv) > 1:
                self.apod_date = sys.argv[1]

                # Check if the date is in the correct format
                self.apod_date = datetime.strptime(self.apod_date, '%Y-%m-%d').date()

                # Check if the date is in the future
                if datetime.strptime(self.apod_date.isoformat(), '%Y-%m-%d') > datetime.strptime(date.today().isoformat(), '%Y-%m-%d'):
                    print('Date cannot be in the future')
                    sys.exit()
                
                # Convert date to string
                self.apod_date = self.apod_date.isoformat()
            else:
                self.apod_date = date.today().isoformat()
        except ValueError as err:
            print(err)
            
    def init_apod_cache(self):

        self.image_cache_dir = os.path.join('image_cache')
        self.image_cache_db = os.path.join(
            self.image_cache_dir, 'image_cache.db')

        os.makedirs(self.image_cache_dir, exist_ok=True)
        if not os.path.exists(self.image_cache_db):
            with open(self.image_cache_db, 'w') as f:
                pass

            f.close()
            # Creating table
            conn = sqlite3.connect(self.image_cache_db)
            create_table_query = '''
                CREATE TABLE IF NOT EXISTS apod_cache (
                    date DATE,
                    title TEXT,
                    explanation TEXT,
                    image_path TEXT,
                    sha256 TEXT
                );
            '''
            conn.execute(create_table_query)
            conn.commit()
            conn.close()

    def add_apod_to_cache(self):
        # TODO: Download the APOD information from the NASA API
        loader = APILoader(self.apod_date)
        apod_data = loader.get_apod_info()
        image_url = loader.get_apod_image_url()

        # TODO: Download the APOD image
        imglib = ImageLib(image_url)

        # TODO: Check whether the APOD already exists in the image cache
        conn = sqlite3.connect(self.image_cache_db)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM apod_cache WHERE date = ?',
            (self.apod_date, )  #comma pan jruri che
        )
        existing_apod = cursor.fetchall()
        conn.commit()
        conn.close()
        if existing_apod:
            print('APOD already exists in the cache.')

        if not existing_apod:
            # TODO: Save the APOD file to the image cache directory
            image_filename = os.path.basename(image_url)
            image_path = os.path.join(self.image_cache_dir, image_filename)
            imglib.download_image()
            imglib.save_image(image_path)

            # TODO: Add the APOD information to the DB
            self.add_apod_to_db(apod_data['title'], apod_data['explanation'], image_path, loader.get_sha256())

    def add_apod_to_db(self, title, explanation, file_path, sha256):
        try:
            conn = sqlite3.connect(self.image_cache_db)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO apod_cache (date, title, explanation, image_path, sha256) VALUES (?, ?, ?, ?, ?)",
                (self.apod_date, title, explanation, file_path, sha256)
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as err:
            print(err)



    def get_all_apod_titles(self):
        conn = sqlite3.connect(self.image_cache_db)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT title FROM apod_cache'
            )
        titles = cursor.fetchall()
        conn.commit()
        conn.close()
        return titles


if __name__ == '__main__':
    obj = APOD()
    obj.get_apod_date()
    print(obj.apod_date)
    obj.init_apod_cache()
    obj.add_apod_to_cache()
