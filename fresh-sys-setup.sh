echo "

 ... Downloading webmin"
wget http://prdownloads.sourceforge.net/webadmin/webmin_1.680_all.deb
sudo apt-get install perl libnet-ssleay-perl openssl libauthen-pam-perl libpam-runtime libio-pty-perl apt-show-versions libapt-pkg-perl
sudo dpkg --install webmin_1.680_all.deb
rm webmin_1.680_all.deb
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


