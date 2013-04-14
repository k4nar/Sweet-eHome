libs = [
    'DumbDevicesLib',
    #'ZwaveLib',
]

def get_all_wrappers(*args, **kwargs):
    wrappers = {}

    for lib in libs:
        try:
            driver = __import__(lib).Driver(*args, **kwargs)

            wrappers[driver.name] = driver

        except Exception, e:
            print "Can't import module", lib, ':', e

    return wrappers
