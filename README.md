# Omission

A game where you find what letter has been removed from a passage.

## Content Notes

The content for this game has been derived from "Bartlett's Familiar Quotations".

For brevity, the source of each quote has been omitted - both title and author.

Sections previously italicized have been replaced with CAPS for easier
display.

Passages have been trimmed and rearranged to be no more than 4-5 lines.

## Authors

 - Jason C. McDonald
 - Jarek G. Thomas
 - Anne McDonald (Content)
 - Jane McArthur (Content)

## Dependencies

 - Python3
 - Kivy >= 1.10
 - appdirs >= 1.4.3

## Setup

### Windows 7 and later

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

7. Download the .zip for Omission and put it in your main user folder.
Right-click the file, click "Extract All", and follow the instructions.

8. In your command prompt, we'll start Omission.

~~~
cd omission
python -m omission
~~~

**Every time you want to run Omission again, open a new command prompt
and follow ONLY step 8 again!**

### Mac OS X/appleOS

We'll be using Homebrew to set up our Python environment.

1. Open the Terminal application.

~~~
Future sections that look like this
should be typed in the Terminal,
followed by the ENTER key.
(Don't type this one in.)
~~~

2. Start by installing Python 3 on Homebrew.

~~~
brew install python3
~~~

3. Install the dependencies for Kivy.

~~~
brew install pkg-config sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer
pip install -U Cython
~~~

4. Install Kivy.

~~~
pip install kivy
~~~

5. Install `appdirs`.

~~~
pip install appdirs
~~~

6. Download the .zip for Omission and put it in your main user folder.
Double-click it to unzip it.

7. In your Terminal, we'll start Omission.

~~~
cd omission
python3 -m omission
~~~

**Every time you want to run Omission again, open a new Terminal
and follow ONLY step 7 again!**

### Ubuntu/Linux Mint

1. Open the Terminal application.

~~~
Future sections that look like this
should be typed in the Terminal,
followed by the ENTER key.
(Don't type this one in.)
~~~

2. Make sure Python 3 is installed.

~~~
sudo apt-get update
sudo apt-get install python3
~~~

3. Install Kivy using their repository.

~~~
sudo add-apt-repository ppa:kivy-team/kivy
sudo apt-get update
sudo apt-get install python3-kivy
~~~

4. Install `appdirs`

~~~
sudo apt-get install python3-appdirs
~~~

5. Download the .zip for Omission and put it in your main user folder.
Right-click it and select `Extract Here`.

6. In your Terminal, we'll start Omission.

~~~
cd omission
python3 -m omission
~~~

**Every time you want to run Omission again, open a new Terminal
and follow ONLY step 7 again!**

### Debian Jessie

1. Open the Terminal application.

~~~
Future sections that look like this
should be typed in the Terminal,
followed by the ENTER key.
(Don't type this one in.)
~~~

2. Make sure Python 3 is installed.

~~~
sudo apt-get update
sudo apt-get install python3
~~~

3. Install Kivy using their repository.

~~~
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
echo "deb http://ppa.launchpad.net/kivy-team/kivy/ubuntu trusty main" | sudo tee -a /etc/apt/sources.list
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A863D2D6
sudo apt-get update
sudo apt-get install python3-kivy
~~~

4. Install `appdirs`

~~~
sudo apt-get install python3-appdirs
~~~

For more information, see [Kivy's official installation instructions for Debian](https://kivy.org/docs/installation/installation-linux.html#debian-jessie-or-newer)

5. Download the .zip for Omission and put it in your main user folder.
Right-click it and select `Extract Here`.

6. In your Terminal, we'll start Omission.

~~~
cd omission
python3 -m omission
~~~

**Every time you want to run Omission again, open a new Terminal
and follow ONLY step 7 again!**

### Other Systems

If you're running Fedora, OpenSUSE, or a virtual environment on just about any
modern operating system, you can still run Omission. You will need to be running
Python 3, the ``appdirs`` Python package (installable via ``pip``), as well
as Kivy and its dependencies.

[Full installation instructions for Kivy can be found on their website](https://kivy.org/docs/installation/installation.html).

Finally, download and extract the .zip for Omission, navigate into it,
and execute it via `python3 -m omission` (or whatever similar as appropriate
for your environment.)

## Contributions

We do NOT accept pull requests through GitHub.
If you would like to contribute code, please read our
[Contribution Guide][3].

All contributions are licensed to us under the
[MousePaw Media Terms of Development][4].

## License

Omission is licensed under the BSD-3 License. (See LICENSE.md)

The project is owned and maintained by [MousePaw Games][1],
a subsidiary of [MousePaw Media][2].

[1]: https://www.mousepawgames.com/omission
[2]: https://www.mousepawmedia.com/developers
[3]: https://www.mousepawmedia.com/developers/contribution
[4]: https://www.mousepawmedia.com/termsofdevelopment
[5]: https://github.com/mousepawmedia/omission
