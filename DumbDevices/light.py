from device import Device


class Light(Device):
    def __init__(self, id="",
                        dummer=False, var=None,
                        changeColor=False, color=None):
        Device.__init__(self, id)

        self.type = "Light"

        self.properties["on"] = True
        self.properties["var"] = var
        self.properties["color"] = color

        self.actions["turnOn"] = self.turnOn
        self.actions["turnOff"] = self.turnOff
        self.actions["toggle"] = self.toggle
        if dummer:
            self.actions["variate"] = self.variate
        if changeColor:
            self.actions["changeColor"] = self.changeColor

    def turnOn(self, *args):
        self.properties["on"] = True
        return True

    def turnOff(self, *args):
        self.properties["on"] = False
        return True

    def toggle(self, *args):
        self.properties["on"] = not self.properties["on"]
        return True

    def variate(self, var, *args):
        if var >= 0 and var <= 1:
            self.properties["var"] = var
            return True
        return False

    def changeColor(self, color, *args):
        if color in ["red", "blue", "green", "yellow"]:
            self.properties["color"] = color
            return True
        return False
