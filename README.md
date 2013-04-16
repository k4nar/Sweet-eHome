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

### DumbDevices
DumbDevices is a test purpose protocol. It's only intended to be used to test and debug Sweet-eHome. If you want to try it, you can get it [there](lolo.com)

### Others
We need people to implement other protocols, feel free to contribute !
