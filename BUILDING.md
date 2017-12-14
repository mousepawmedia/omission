# Building

Use these instructions to run Omission from the repository. These should
work in nearly all cases.

If you run into trouble, contact support@mousepawmedia.com

## Windows 7 and later

1. [Download the latest Python 3 Release](https://www.python.org/downloads/windows/)
and install it on your computer. Choose `Customize Installation`, use the
defaults on the first page, and additionally check `Add Python to Environment Path`
on the second page.

2. Open your command prompt by searching for the program `cmd`.

~~~
Future sections that look like this
should be typed in command prompt,
followed by the ENTER key.
(Don't type this one in.)
~~~

3. Upgrade `pip`, the Python package tool.

~~~
python -m pip install --upgrade pip wheel setuptools
~~~

NOTE: If you get an error about 'api-ms-win-crt-runtime-l1-1-0.dll',
make sure your computer is up-to-date.

4. Install `appdirs` using pip:

~~~
python -m pip install appdirs
~~~

5. Install Kivy's dependencies.

~~~
python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew kivy.deps.gstreamer
~~~

6. Install Kivy itself.

~~~
python -m pip install kivy
~~~

7. Download the .zip for Omission and put it directly on the `C:` drive.
Right-click the file, click "Extract All", and follow the instructions.

8. In your command prompt, we'll start Omission.

~~~
cd C:\omission-master\omission-master
python -m omission
~~~

**Every time you want to run Omission again, open a command prompt
and follow ONLY step 8 again!**

## macOS/Mac OS X 10.7.5 Lion or later

We'll be using Macports to set up our Python environment.

1. Install Xcode from your App Store. If it reports that your system is
too old, you can download the version for your OS from [developer.apple.com/download](https://developer.apple.com/download).

2. Download Macports for your operating system from [the MacPorts website](https://www.macports.org/install.php). Install it on your system.

3. Open the Terminal application, which is under Utilities.

~~~
Future sections that look like this
should be typed in the Terminal,
followed by the ENTER key.
(Don't type this one in.)
~~~

4. Install Python 3.6, and set it as your new default. We'll do the same
for `pip`, Python's package installer.

~~~
sudo port install python36
sudo port select --set python python36
sudo port install py36-pip
sudo port select --set pip pip36
~~~

5. Install the dependencies for Kivy.

~~~
sudo port install libsdl2 libsdl2_image libsdl2_ttf libsdl2_mixer
pip install -U Cython
pip install Pillow pygame
~~~

6. Install Kivy.

~~~
pip install kivy
~~~

7. Install `appdirs`.

~~~
pip install appdirs
~~~

8. Download the .zip for Omission. We'll leave it in Downloads for convenience.
In your Finder, double-click it to unzip it.

9. In your Terminal, we'll start Omission.

~~~
cd ~/Downloads/omission-master; python -m omission
~~~

**Every time you want to run Omission again, open a Terminal
and follow ONLY step 9 again!**

## Linux

1. Open the Terminal application.

~~~
Future sections that look like this
should be typed in the Terminal,
followed by the ENTER key.
(Don't type this one in.)
~~~

2. Make sure Python 3 and virtualenv are installed. On a Debian-based system,
run...

~~~
sudo apt-get update
sudo apt-get install python3 virtualenv
~~~

3. Install Kivy's system dependencies. On a Debian-based system, you can run...

~~~
sudo apt-get install ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev libgstreamer1.0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good
~~~

3. Ensure you are in the Omission repository directory, and run the Makefile:

~~~
make
~~~

The output directory is `/dist/Omission`.

4. To start Omission from your Terminal, run the following from within the
Omission repository...

~~~
dist/Omission/Omission
~~~
