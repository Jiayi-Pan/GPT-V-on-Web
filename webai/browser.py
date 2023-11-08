from selenium import webdriver 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from io import BytesIO
from PIL import Image

from time import sleep
import os
import base64
import platform
import re

def get_cache_directory():
    """
    Get the cache directory based on the operating system.
    """
    if platform.system() == 'Windows':
        return os.path.join(os.environ['LOCALAPPDATA'], 'Cache')
    elif platform.system() == 'Darwin':
        return os.path.join(os.path.expanduser('~'), '.cache')
    else:
        return os.path.join(os.path.expanduser('~'), '.cache')


cache_dir = get_cache_directory()


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_temp_img_path():
    return cache_dir + "/current_view.png"

class Browser:
    def __init__(self, start_link, resolution):
        # enable vimium and start browser
        options = webdriver.ChromeOptions()
        options.add_extension(os.path.dirname(os.path.realpath(__file__)) + "/vimium.crx")
        self.driver = webdriver.Chrome(options=options)
        # set window size and start link
        self.driver.set_window_size(resolution[0], resolution[1])
        self.driver.get(start_link)
        self.actions = ActionChains(self.driver)
        sleep(1)
        # do an initial escape press
        self.actions.send_keys(Keys.ESCAPE)
        self.lastest_view = None
    
    def save_current_view(self)-> None:
        # TOFIX: why sometimes it fails to save the image?
        # self.lastest_view = self.driver.get_screenshot_as_base64()
        # has_suc = self.driver.get_screenshot(get_temp_img_path())
        # if not has_suc:
        #     raise Exception("Failed to save current view!")
        # self.lastest_view = base64.b64encode(png_bin).decode('utf-8')

    # Convert the binary data to a PIL Image object
        png_bin = self.driver.get_screenshot_as_png()
        image = Image.open(BytesIO(png_bin))
        image.save("test.png")

        # Create a buffer to hold the JPEG image data
        jpeg_buffer = BytesIO()

        # Save the image as JPEG to the buffer
        image = image.convert('RGB')
        image.save(jpeg_buffer, format="JPEG")

        # Get the byte data from the buffer
        jpeg_data = jpeg_buffer.getvalue()

        # Encode the JPEG image data in base64
        jpg_base64 = base64.b64encode(jpeg_data)

        # If you need it in string format
        jpg_base64_str = jpg_base64.decode('utf-8')

        self.lastest_view = jpg_base64_str

        # png_bin = self.driver.get_screenshot_as_png()
        # image = Image.open(BytesIO(png_bin))
        # image.save(get_temp_img_path())


    def get_obs_msg(self)-> dict:
        # base64_image = encode_image(get_temp_img_path())
        base64_image = self.lastest_view
        msg = {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}"
            }
        }
        return msg
    
    def step(self, action) -> None:
        parts = re.split('(<[^>]+>)', action)

        try:
            sleep(1)
            for part in parts:
                # Check if the part is a special key
                if part.startswith('<') and part.endswith('>'):
                    # Translate special keys to ActionChains methods
                    if part == '<DELETE>':
                        self.actions.send_keys(Keys.BACKSPACE)
                    elif part == '<ENTER>':
                        self.actions.send_keys(Keys.ENTER)
                    # Add more special keys if needed
                else:
                    # Send regular text
                    self.actions.send_keys(part)
            self.actions.perform()
        except Exception as e:
            print(e)
            pass