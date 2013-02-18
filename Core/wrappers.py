import DumbDevicesLib

libs = {
    "DumbDevices": 'DumbDevicesLib',
}

wrappers = {}

for name, module_name in libs:
    try:
        module = __import__(module_name)

        wrappers[name] = {
            "listener": module.listener(),
            "sender": module.sender(),
            "broadcaster": module.broadcaster()
        }
        
    except:
        pass
