import sys
import pyzed.sl as sl
from PIL import Image
import torch

def capture(imagePath):
	#Create a ZED camera object
	zed = sl.Camera()
	
	# Set configuration parameters
	init_params = sl.InitParameters()
	init_params.depth_mode = sl.DEPTH_MODE.DEPTH_MODE_ULTRA # Use ULTRA depth mode
	init_params.coordinate_units = sl.UNIT.UNIT_INCH # Use millimeter units (for depth measurements)
	
	#Open the camera
	err = zed.open(init_params)
	if err != sl.ERROR_CODE.SUCCESS:
		print("[DECON] Error: Unable to open the camera")
		zed.close()
		exit(-1)
	
	try:
		image = sl.Mat()
		depth_map = sl.Mat()
		runtime_parameters = sl.RuntimeParameters()
		if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS :
			# A new image and depth is available if grab() returns SUCCESS
			zed.retrieve_image(image, sl.VIEW.VIEW_LEFT) # Retrieve left image
			img = image.get_data()
			im = Image.fromarray(img).rotate(180)
		im.save(imagePath)
                del im	
	except Exception as e:
		print("[DECON] Error: Exception occured")
		print(e)
	finally:
		torch.cuda.empty_cache()
		zed.close()

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("[DECON] Error: Correct command is python2.7 camera.py <imagePath>")
	else:
		capture(sys.argv[1])
