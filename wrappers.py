libs = {
    "DumbDevices": 'DumbDevicesLib',
    "Zwave": "ZwaveLib",
}

def get_all_wrappers(*args, **kwargs):
    wrappers = {}

    for name, module_name in libs.items():
        try:
            module = __import__(module_name)

            print dir(module)
            print module.__name__
            print module.__package__

            wrappers[name] = {
                "listener": module.listener.Listener(*args, **kwargs),
                "sender": module.sender.Sender(*args, **kwargs),
                "broadcaster": module.broadcaster.Broadcaster(*args, **kwargs)
            }
            
        except Exception, e:
            print "Can't import module", module_name, ':', e

    return wrappers
