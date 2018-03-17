#!/bin/bash
INSTALL_DIR=/opt/com/mousepawmedia/omission
echo "Installing Omission AppImage to /opt/omission..."
sudo mkdir -p ${INSTALL_DIR}
sudo cp Omission-*.AppImage ${INSTALL_DIR}/Omission.AppImage
sudo chmod +x ${INSTALL_DIR}/Omission.AppImage
sudo cp omission.png ${INSTALL_DIR}/omission.png
sudo cp uninstall.sh ${INSTALL_DIR}/uninstall.sh
echo "Installing .desktop file to /usr/share/applications..."
sudo cp *.desktop /usr/share/applications/
echo "Creating symlink in /usr/bin..."
sudo ln -s ${INSTALL_DIR}/launch.sh /usr/bin/omission
echo "Install complete! Enjoy your software."