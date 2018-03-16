#!/bin/bash
echo "Removing /opt/omission..."
sudo rm -rf /opt/omission
echo "Removing .desktop file..."
sudo rm -f /usr/share/applications/omission.desktop
echo "Omission has been removed from your system."