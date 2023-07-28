#!/bin/bash

# based off of adafruit's install script
# https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/rgb-matrix.sh
# modified by totallynotmark6 to have no user input

# INSTALLER SCRIPT FOR ADAFRUIT RGB MATRIX BONNET

# hzeller/rpi-rgb-led-matrix sees lots of active development!
# That's cool and all, BUT, to avoid tutorial breakage,
# we reference a specific commit (update this as needed):
GITUSER=https://github.com/hzeller
REPO=rpi-rgb-led-matrix
COMMIT=45d3ab5d6cff6e0c14da58930d662822627471fc #needs updated if This is merged/Released 

if [ $(id -u) -ne 0 ]; then
	echo "Installer must be run as root."
	echo "Try 'sudo bash $0'"
	exit 1
fi

HAS_PYTHON2=$( [ ! $(which python2) ] ; echo $?)
HAS_PYTHON3=$( [ ! $(which python3) ] ; echo $?)

# FEATURE PROMPTS ----------------------------------------------------------

INTERFACE_TYPE=0 
QUALITY_MOD=1

INTERFACES=( \
  "Adafruit RGB Matrix Bonnet" \
  "Adafruit RGB Matrix HAT + RTC" \
)

QUALITY_OPTS=( \
  "Quality (disables sound, requires soldering)" \
  "Convenience (sound on, no soldering)" \
)

# VERIFY SELECTIONS BEFORE CONTINUING --------------------------------------

echo
echo "Interface board type: ${INTERFACES[$INTERFACE_TYPE]}"

echo "Optimize: ${QUALITY_OPTS[$QUALITY_MOD]}"
if [ $QUALITY_MOD -eq 0 ]; then
	echo "Reminder: you must SOLDER a wire between GPIO4"
	echo "and GPIO18, and internal sound is DISABLED!"
fi
echo

# START INSTALL ------------------------------------------------------------
# All selections are validated at this point...

# Given a filename, a regex pattern to match and a replacement string,
# perform replacement if found, else append replacement to end of file.
# (# $1 = filename, $2 = pattern to match, $3 = replacement)
reconfig() {
	grep $2 $1 >/dev/null
	if [ $? -eq 0 ]; then
		# Pattern found; replace in file
		sed -i "s/$2/$3/g" $1 >/dev/null
	else
		# Not found; append (silently)
		echo $3 | sudo tee -a $1 >/dev/null
	fi
}

echo
echo "Starting installation..."
echo "Updating package index files..."
apt-get update

echo "Downloading prerequisites..."
if [ $HAS_PYTHON2 ]; then
	apt-get install -y --force-yes python2.7-dev python-pillow
fi
if [ $HAS_PYTHON3 ]; then
	apt-get install -y --force-yes python3-dev python3-pillow
fi

echo "Downloading RGB matrix software..."
curl -L $GITUSER/$REPO/archive/$COMMIT.zip -o $REPO-$COMMIT.zip
unzip -q $REPO-$COMMIT.zip
rm $REPO-$COMMIT.zip
mv $REPO-$COMMIT rpi-rgb-led-matrix
echo "Building RGB matrix software..."
cd rpi-rgb-led-matrix
USER_DEFINES=""

if [ $QUALITY_MOD -eq 0 ]; then
	if [ $HAS_PYTHON2 ]; then
		# Build and install for Python 2.7...
		make clean
		make install-python HARDWARE_DESC=adafruit-hat-pwm USER_DEFINES="$USER_DEFINES" PYTHON=$(which python2)
	fi
	if [ $HAS_PYTHON3 ]; then
		# Do over for Python 3...
		make clean
		make install-python HARDWARE_DESC=adafruit-hat-pwm USER_DEFINES="$USER_DEFINES" PYTHON=$(which python3)
	fi
else
	USER_DEFINES+=" -DDISABLE_HARDWARE_PULSES"
	if [ $HAS_PYTHON2 ]; then
		# Build then install for Python 2.7...
		make clean
		make install-python HARDWARE_DESC=adafruit-hat USER_DEFINES="$USER_DEFINES" PYTHON=$(which python2)
	fi
	if [ $HAS_PYTHON3 ]; then
		# Do over for Python 3...
		make clean
		make install-python HARDWARE_DESC=adafruit-hat USER_DEFINES="$USER_DEFINES" PYTHON=$(which python3)
	fi
fi
# Change ownership to user calling sudo
chown -R $SUDO_USER:$(id -g $SUDO_USER) `pwd`


# CONFIG -------------------------------------------------------------------

echo "Configuring system..."

if [ $QUALITY_MOD -eq 0 ]; then
	# Disable sound ('easy way' -- kernel module not blacklisted)
	reconfig /boot/config.txt "^.*dtparam=audio.*$" "dtparam=audio=off"
else
	# Enable sound (ditto)
	reconfig /boot/config.txt "^.*dtparam=audio.*$" "dtparam=audio=on"
fi

# PROMPT FOR REBOOT --------------------------------------------------------

echo "Done."
echo
echo "Settings take effect on next boot."
exit 0
