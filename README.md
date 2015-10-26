Dashcam
=======

Install
-------
### Install Dashcam Services
~~~bash
sudo cp ~/dashcam/etc/systemd/user/*.service /etc/systemd/system/
sudo systemctl enable dashcam-cleaner.service
sudo systemctl enable dashcam.service
~~~
