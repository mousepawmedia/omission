PREFIX = /opt

none:
	@echo "=== Omission 1.0 ==="
	@echo "Select a build target:"
	@echo "  make build           Create a pyinstaller binary in a virtualenv."
	@echo "  make clean           Remove the build files."
	@echo "  make distclean       Remove the build files, virtualenv, AND final files."
	@echo "  make appimage        Package as AppImage. Requires APPIMAGETOOL to be specified."
	@echo
	@echo "  make appimage_check  Ensure APPIMAGETOOL is a valid path."
	@echo "  make appimage_pre    Prepare the build files for AppImage packaging."
	@echo "  make appimage_build  Prepare the build files for AppImage packaging."
	@echo "  make appimage_post   Tarball the AppImage with it's install scripts for deployment."

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
	@echo "\033[1mCleaning up deployment files.\033[0m"
	@rm Omission-x86_64.AppImage
	@rm Omission.tar.gz

.PHONY: appimage
appimage: appimage_check build appimage_prep appimage_build appimage_post
	@echo "AppImage created! See Omission.tar.gz"

.PHONY: appimage_check
appimage_check:
	@test -s ${APPIMAGETOOL}
	@echo "appimagetool location confirmed."

.PHONY: appimage_prep
appimage_prep:
	@mkdir -p dist/Omission.AppDir/usr/bin
	@cp -rf dist/Omission/* dist/Omission.AppDir/usr/bin
	@chmod +x -R dist/Omission.AppDir
	@cp appimage/AppRun dist/Omission.AppDir/
	@cp appimage/omission.png dist/Omission.AppDir/
	@cp appimage/omission.desktop dist/Omission.AppDir/
	@echo "Run appimagetool on the dist/Omission.AppDir folder to package."

.PHONY: appimage_build
appimage_build:
	@test -s ${APPIMAGETOOL}
	@${APPIMAGETOOL} dist/Omission.AppDir
	@echo "AppImage created!"

.PHONY: appimage_post
appimage_post:
	@test -s Omission-*.AppImage
	@mkdir -p dist/deploy
	@cp -f Omission-*.AppImage dist/deploy/
	@cp -rf deploy_linux/* dist/deploy/
	@tar -cvzf Omission.tar.gz -C dist/deploy .
	@echo "Deployment tarball created!"
