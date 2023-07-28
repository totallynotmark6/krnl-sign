sudo apt install -y python3-pip git
git clone https://github.com/totallynotmark6/krnl-sign.git
cd krnl-sign
sudo ./rgbmatrixinstall.sh
sudo -H python3 -m pip install -e ./krnl-sign
sudo cp -v ./bin/krnl-sign.service /lib/systemd/system/
sudo systemctl enable krnl-sign.service
sudo restart
