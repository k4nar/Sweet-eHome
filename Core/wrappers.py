import DumbDevicesLib

libs = {
    "DumbDevices": 'DumbDevicesLib',
}

def get_all_wrappers(wrappers):
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

wrappers = {}
get_all_wrappers(wrappers)
