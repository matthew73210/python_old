This app is used to monitor a boiler via an OTGW (http://otgw.tclcode.com/). Based on a nodeMCU.
The opentherm protocol can be found at : https://www.domoticaforum.eu/uploaded/Ard%20M/Opentherm%20Protocol%20v2-2.pdf

This version is meant to be used via tcp, the code needs changing for ftdi usage. If somebody can try using ftdi I'd happily help.

To use this App the OTGW must have a static ip or a working DNS server (i haven't tried this as of writing). And a defined port in the nodeMCU settings.

After that you need to create in configuration.yaml an input variable which can be used to control the boiler water heating temperature.

You can set the amount of logging in the App, usefull if you want to debug, note that the App logs into the AppDeamon logs.

The App will check if a connection can be made and report an error if it can't, you'll need to check that the nodeMCU host is up and yu have set the right IP/PORT.

After thar the App will poll the boiler stats every XX seconds, which can be set in :
self.run_every(self.run_opentherm,datetime.now(),XX). 
The default is 20 seconds.

Before each connection the app will check if it can still connect to the host. If it can it will do the read/write functions. If not it'll post to log and wait till the next run command.

Good riddence.
