# to automatically run this at boot, use the command: crontab -e
# then add this line at the bottom: @reboot /home/pi/piWebRadio/run.sh &

cd /home/pi/piWebRadio
../pythonenv/bin/python waitUntilNetworkReady.py
../pythonenv/bin/waitress-serve --port=6513 'piWebRadio:app' &
