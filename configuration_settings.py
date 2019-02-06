
class ConfigurationSettings:

    def __init__(self):
        self.settings = self.configDictionary(self.readFile("../Settings/config.txt"))


    # Takes a newline delimited list of config settings, turns them into
    # a string dictionary of {configName : configSetting}
    def configDictionary(self, configLines):
        configDict = {}
        for line in configLines:
            setting = line.split("=")
            configDict[setting[0]] = setting[1]

        return configDict

    # Generic function for reading a file and splitting by newline
    def readFile(self, fileName):
        f = open(fileName)
        lines = f.read().splitlines()
        f.close()
        return lines

