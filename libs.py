from logger import logger

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
            logger.warning("Can't import module {}: {}".format(lib, e))

    return wrappers
