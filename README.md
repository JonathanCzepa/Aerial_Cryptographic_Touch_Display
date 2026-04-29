# ~~~~~~~~~~~~~~~~~~~ Hardware ~~~~~~~~~~~~~~~~~~~

This project utilizes four main hardware components, the three needed to create a floating image are an LCD, retroreflector material, and a beam splitter. When choosing these three it is important to note that if you want the entire screen reflected back both the retroreflector and beamsplitter need to be equal or larger than the LCD to get the whole image.

	LCD: 
	https://www.waveshare.com/7inch-hdmi-lcd-h.htm 

A 1024 x 600 7inch LCD was used as anything larger would be to large to properly use, and anything smaller would make the keypad functionality hard to implement. It is ideal to get as high of a resolution as possible, along with as bright of a screen as possible for best outcome. 

	Retroreflective Material: https://americansignproducts.com/product/3m-3930-white-high-intensity-prismatic-reflective-sheeting/ -> 

This was the best product available in the US, ideally it should be replaced with a smooth retroreflector as the design on the tape appears to cause a slight bluriness to the produced image.

	Beam Splitter: https://glidegear.net/products/teleprompter-replacement-glass -> 

It appears that the best option for small beam splitter glass is teleprompter replacement glass, most of which comes in atleast 7inch sizes.

	Computing Board (Pi 4B): https://www.mouser.com/c/embedded-solutions/computing/?form%20factor=Raspberry%20Pi%204%20B&utm_id=22019481498&utm_source=google&utm_medium=cpc&utm_marketing_tactic=amercorp -> 

The computing board chosen was a PI4B for its ease of use and its capable I/O. This should be capeable of running off of any Windows/Linux Machine with little change.

TOF Sensor: https://www.digikey.com/en/products/detail/stmicroelectronics/VL53L5CX-SATEL/14552430 -> 

These come packaged as a product of two so only one purchase is necessary. It was initially hoped that a single sensor would be able to give enough information for both row and column, but both sensors had to be used, one for row detection and another for column detection.

# ~~~~~~~~~~~~~~~~~~~ Software ~~~~~~~~~~~~~~~~~~~

Start the vnev:     

	python3 -m venv display

Activate the venv:  

	source display/bin/activate

Tkinter:     

	pip install tkinter 

Numpy:      

	pip install numpy 

TOF Sensor:  

	pip install qwiic_vl53l5cx

Math:        

	pip install math 
