#!/bin/bash
echo "Removing /opt/omission..."
sudo rm -rf /opt/com/mousepawmedia/omission
echo "Removing .desktop file..."
sudo rm -f /usr/share/applications/com.mousepawmedia.omission.desktop
echo "Removing /usr/bin symlink..."
sudo rm -f /usr/bin/omission
echo "Omission has been removed from your system."