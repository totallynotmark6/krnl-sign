git clone https://github.com/totallynotmark6/krnl-sign.git
cd krnl-sign
sudo -H python3 -m pip install -e .
sudo cp -v ./bin/krnl-sign.service /lib/systemd/system/
sudo systemctl enable krnl-sign.service
sudo systemctl start krnl-sign.service
