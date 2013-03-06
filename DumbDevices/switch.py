from device import Device


class Switch(Device):
    def __init__(self, id=""):
        Device.__init__(self, id)

        self.type = "Switch"

        self.properties["on"] = True

        self.actions["turnOn"] = self.turnOn
        self.actions["turnOff"] = self.turnOff
        self.actions["toggle"] = self.toggle

    def turnOn(self):
        self.properties["on"] = True
        return True

    def turnOff(self):
        self.properties["on"] = False
        return True

    def toggle(self):
        self.properties["on"] = not self.properties["on"]
        return True
