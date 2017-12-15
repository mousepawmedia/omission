PREFIX = /opt

none: build

.PHONY: build
# Create a virtual environment for Python3 and use it for building
build: clean
	@echo "\033[1mBuilding Omission.\033[0m"
	@( \
		mkdir -p buildvenv/home; \
		export HOME=$$(pwd)/buildvenv/home; \
		virtualenv --no-site-packages -p python3 buildvenv; \
		# in sh, `.` == `source` (bash). This still works in bash. \
		. buildvenv/bin/activate; \
		pip install -U pip; \
		pip install pyinstaller cython==0.25.2; \
		pip install -r requirements.txt; \
		pyinstaller omission.spec -y; \
		deactivate; \
		sh ./strip.sh; \
	)

.PHONY: clean
# Remove the virtualenv and the built files.
clean:
	@echo "\033[1mCleaning up build files.\033[0m"
	@rm -rf build/
	@rm -rf dist/

.PHONY: distclean
# Remove the virtualenv AND the built files.
distclean: clean
	@echo "\033[1mCleaning up virtualenv.\033[0m"
	@rm -rf buildvenv/

.PHONY: install
install:
	mkdir -p $(DESTDIR)$(PREFIX)
	cp -r dist/Omission $(DESTDIR)$(PREFIX)/omission

.PHONY: tarball
tarball: distclean
	git archive --format=tar.gz master > ../omission_1.0-1.orig.tar.gz
