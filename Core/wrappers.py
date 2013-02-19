import DumbDevicesLib

libs = {
    "DumbDevices": 'DumbDevicesLib',
}

wrappers = {}

for name, module_name in libs:
    try:
        module = __import__(module_name)

        wrappers[name] = {
            "listener": module.Listener(),
            "sender": module.Sender(),
            "broadcaster": module.Broadcaster()
        }
        
    except:
        pass
