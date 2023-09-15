import subprocess

def set_wallpaper(image_path):
    # Set the wallpaper using dconf
    subprocess.Popen(['dconf', 'write',
                      '/org/gnome/desktop/background/picture-uri',
                      "'file://{}'".format(image_path)])

# Example usage
set_wallpaper('/home/brijesh/Desktop/apod-final/image_cache/DracoTrio_TeamOmicron.jpg')