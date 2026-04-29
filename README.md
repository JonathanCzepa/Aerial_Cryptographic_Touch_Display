# ~~~~~~~~~~~~~~~~~~~ Hardware ~~~~~~~~~~~~~~~~~~~

This project utilizes four main hardware components, the three needed to create a floating image are an LCD, retroreflector material, and a beam splitter. When choosing these three it is important to note that if you want the entire screen reflected back both the retroreflector and beamsplitter need to be equal or larger than the LCD to get the whole image.

LCD:
https://www.waveshare.com/7inch-hdmi-lcd-h.htm  ->  This porject utilized a 1024 x 600 7inch LCD as anyhting larger would be to large to properly use, and anything smaller would make the keypad functionality hard to implement. It is ideal to get as high of a resolution as possible, along with as bright of a screen as possible for best outcome. 

Retroreflective Material:
https://americansignproducts.com/product/3m-3930-white-high-intensity-prismatic-reflective-sheeting/ -> This was the best product available in the US, ideally it should be replaced with a smooth retroreflector as the design on the tape appears to cause a slight bluriness to the produced image.


Beam Splitter:
https://glidegear.net/products/teleprompter-replacement-glass -> It appears that the best option for small beam splitter glass is teleprompter replacement glass. 

When choosing all three of the above hardware it is important that the size matches the LCD as you want to reflect all of the LCD screen, so choosing a retroreflector and beamsplitter larger than the LCD is advised

As this project intends to make a floating keypad it needs to utilize a TOF sensor, or 2, to detect a finger "pressing" on the keypad. 

# ~~~~~~~~~~~~~~~~~~~ Software ~~~~~~~~~~~~~~~~~~~



# Aerial_Cryptographic_Touch_Display
https://github.com/sparkfun/qwiic_vl53l5cx_py
https://github.com/pimoroni/vl53l5cx-python
