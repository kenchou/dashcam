Dashcam
=======

Install
-------
### Install Services
~~~bash
mkdir -p ~/.config/systemd/user
cp ~/dashcam/etc/systemd/user/*.service ~/.config/systemd/user
systemctl --user enable dashcam-cleaner.service
systemctl --user enable dashcam.service
~~~
