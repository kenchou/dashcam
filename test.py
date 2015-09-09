import dashcamera
import picamera

__author__ = 'kzhang'

camera = picamera.PiCamera()
dashcam = dashcamera.DashCamera(camera, storage_path='/home/pi/Videos', interval=3, other='test')

dashcam.run()
