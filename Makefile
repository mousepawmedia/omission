PREFIX = /opt

none:
	@echo "=== Omission 1.0 ==="
	@echo "Select a build target:"
	@echo "  make build           Create a pyinstaller binary in a virtualenv."
	@echo "  make clean           Remove the build files."
	@echo "  make distclean       Remove the build files, virtualenv, AND final files."
	@echo "  make appimage        Package as AppImage. Requires TOOL= to be specified."
	@echo "    e.g. 'make appimage TOOL=~/Downloads/appimagetool-x86_64.AppImage'"
	@echo
	@echo "  make appimage_pre    Prepare the build files for AppImage packaging."
	@echo "  make appimage_build  Package the AppImage using the appimagetool (specified with TOOL=)."

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
# Remove the build files.
clean:
	@echo "\033[1mCleaning up build files.\033[0m"
	@rm -rf build/
	@rm -rf dist/

.PHONY: distclean
# Remove the virtualenv AND the built files.
distclean: clean
	@echo "\033[1mCleaning up virtualenv.\033[0m"
	@rm -rf buildvenv/
	@echo "\033[1mCleaning up release files.\033[0m"
	@rm -rf release/

.PHONY: appimage
appimage: build appimage_prep appimage_build
	@echo "AppImage created! See release/Omission.tar.gz"

.PHONY: appimage_prep
appimage_prep:
	@echo "Removing extraneous files..."
	@rm -rf dist/Omission/build
	@rm -rf dist/Omission/deploy_linux
	@rm -rf dist/Omission/deploy_windows
	@rm -rf dist/Omission/codealike.json
	@echo "Creating AppDir..."
	@cp -rf deploy_linux/appimage dist/Omission.AppDir
	@cp -rf dist/Omission/* dist/Omission.AppDir/usr/bin
	@chmod +x -R dist/Omission.AppDir
	@echo "Run appimagetool on the dist/Omission.AppDir folder to package."

.PHONY: appimage_build
appimage_build:
	@test -s ${TOOL}
	@${TOOL} dist/Omission.AppDir
	@mkdir -p release
	@mv -f Omission*.AppImage release/
	@echo "AppImage created in release/"
