# Derrick

An [ImpactJS](http://impactjs.com/) development server in Twisted Python.
Never again set up apache and php chmod directories to get the Weltmeister
editor just right. This simple development server implements everything the
ImpactJS PHP does, replacing the need for heavyweight environment setup.


### Quick Start

```
$ pip install derrick
```

After installation, derrick will now be available via a twisted plugin, so
simply move to your ImpactJS installation.

```
$ twistd -n derrick
```

A server will now be running at http://localhost:8080. Navigate to
http://localhost:8080/editor to see Weltmeister in action.

If you'd like to daemonize the server, remove the `-n`.


### Disclaimer

Please, please, **please** don't use this in production. A very cursory
attempt to protect file security was made, and as such is probably not very
robust. Also, there is currently no way to turn off the Weltmeister endpoints,
so you could potentially be opening yourself up to people ruining your levels.
