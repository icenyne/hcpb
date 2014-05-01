echo "

 ... Downloading webmin"
wget http://prdownloads.sourceforge.net/webadmin/webmin-1.680.tar.gz
echo  "... don't forget to install webmin"
echo
echo "

 ... Installing system stuff with apt-get"
sudo apt-get install libgphoto2-2 gphoto2 python-pygame openssh-server samba netatalk

echo
echo "

 ... Installing piggyphoto" 
git clone https://github.com/alexdu/piggyphoto.git
echo ... moving piggyphoto
sudo mv piggyphoto/piggyphoto /usr/lib/python2.7


