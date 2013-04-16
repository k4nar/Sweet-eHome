# Sweet-eHome

Abstract layer for home automation protocols, accessible through a RESTful API.

## Installation
* Download the sources or clone this repo
* `sudo pip -r requirements.txt`
* Install and run a MongoDB server

Now, you can run `server start` to start rocking !

## API
The API is described [here](http://docs.sweetehome.apiary.io/).

## Protocols
### Z-Wave
Currently, [Z-Wave](http://www.z-wave.com/modules/ZwaveStart/) is the only protocol supported.
You just need to install [Py-OpenZWave](https://github.com/maartendamen/py-openzwave), and check that is listed 'ZWaveLib' in `src/libs/libs.py`.

A lot of modules are supported, but you might want to add your own wrappers. Feel free to edit `src/libs/ZwaveLib/zwavedriver.py` and to submit a pull-request when you're done.

### DumbDevices
DumbDevices is a test purpose protocol. It's only intended to be used to test and debug Sweet-eHome. If you want to try it, you can get it [there](https://bitbucket.org/peroux_y/dumbdevices)

### Others
We need people to implement other protocols. All you need is creating your driver in `src/libs`, inheriting from `DomoLib/BaseDriver`.
