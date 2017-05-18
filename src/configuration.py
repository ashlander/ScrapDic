import ConfigParser

class Inputs:
    versions = ["scrapbook15"]
    default = ""

    def __init__(self):
        self.default = self.versions[0]

class Outputs:
    versions = ["freemind09"]
    default = ""

    def __init__(self):
        self.default = self.versions[0]

class Configuration:

    __config = ConfigParser.SafeConfigParser()
    __inputs = Inputs()
    __outputs = Outputs()

    __mainSection = "main"
    __valueInput = "datapath"
    __valueOutput = "outputpath"
    __valueInputVersion = "input_version"
    __valueOutputVersion = "output_version"

    def __init__(self):
        self.__config.add_section( self.__mainSection )
        self.__config.set(self.__mainSection, self.__valueInputVersion, self.__inputs.default)
        self.__config.set(self.__mainSection, self.__valueOutputVersion, self.__outputs.default)

    def printConfiguration(self):
        # List all contents
        print("List all contents")
        config = self.__config
        for section in config.sections():
            print("Section: %s" % section)
            for options in config.options(section):
                print("\t- %s:::%s:::%s" % (options,
                                          config.get(section, options),
                                          str(type(options))))

    def setDataPath(self, path):
        self.__config.set(self.__mainSection, self.__valueInput, path)

    def getDataPath(self):
        return self.__config.get(self.__mainSection, self.__valueInput)

    def setOutputPath(self, path):
        self.__config.set(self.__mainSection, self.__valueOutput, path)

    def getOutputPath(self):
        return self.__config.get(self.__mainSection, self.__valueOutput)

    def getInputVersions(self):
        return self.__inputs.versions

    def getDefaultInputVersion(self):
        return self.__inputs.default

    def getOutputVersions(self):
        return self.__outputs.versions

    def getDefaultOutputVersion(self):
        return self.__outputs.default

    def setInputVersion(self, version):
        self.__config.set(self.__mainSection, self.__valueInputVersion, version)

    def getInputVersion(self):
        return self.__config.get(self.__mainSection, self.__valueInputVersion)


    #def setInputVersion(self, version):
    #    self.__config.set(self.__mainSection, self.__valueScrapBookVersion, self.__inputs.default)


