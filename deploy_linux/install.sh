#!/bin/bash
echo "Installing Omission AppImage to /opt/omission..."
sudo mkdir -p /opt/omission
sudo cp Omission-*.AppImage /opt/omission/Omission.AppImage
sudo chmod +x /opt/omission/Omission.AppImage
sudo cp omission.png /opt/omission/omission.png
sudo cp uninstall.sh /opt/omission/uninstall.sh
echo "Installing .desktop file to /usr/share/applications..."
sudo cp omission.desktop /usr/share/applications/
echo "Install complete! Enjoy your software."