libs = {
    "DumbDevices": 'DumbDevicesLib',
    "Zwave": 'ZwaveLib',
}

def get_all_wrappers(*args, **kwargs):
    wrappers = {}

    for name, lib in libs.items():
        try:
            driver = __import__(lib).Driver

            wrappers[name] = driver(*args, **kwargs)
            
        except Exception, e:
            print "Can't import module", lib, ':', e

    return wrappers
