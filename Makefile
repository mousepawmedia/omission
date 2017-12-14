none: build

build: clean
	# Create a virtual environment for Python3 and use it for building
	( \
		virtualenv --no-site-packages -p python3 buildvenv; \
		# in sh, `.` == `source` (bash). This still works in bash. \
		. buildvenv/bin/activate; \
		pip install -U pip; \
		pip install pyinstaller cython==0.25.2; \
		pip install -r requirements.txt; \
		pyinstaller omission.spec -y; \
		deactivate; \
	)

clean:
	# Remove the virtualenv and the built files.
	rm -rf build/
	rm -rf dist/

cleanall: clean
	# Remove the virtualenv AND the built files.
	rm -rf buildvenv/
