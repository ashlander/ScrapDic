from export import ScrabDict
from configuration import Configuration

class ArgsParser:

    config = Configuration()

    def usage(self):

        usage = """scrapdict -i <input_format> -o <output_format> -s <scrapbookdata> -d <destination>
            scrapbookdata   [mandatory] path to scrapbook data directory
            destination     [mandatory] path to output file
            input formats   = [default: %DefaultInputVersion%] %InputVersions%
            output formats  = [default: %DefaultOutputVersion%] %OutputVersions%
            """

        updates = {
                "%InputVersions%":" ".join(self.config.getInputVersions()),
                "%DefaultInputVersion%":self.config.getDefaultInputVersion(),
                "%OutputVersions%":" ".join(self.config.getOutputVersions()),
                "%DefaultOutputVersion%":self.config.getDefaultOutputVersion()
                }

        for old, new in updates.iteritems():
            usage = usage.replace(old, new)

        return usage

    def parse(self, argv):
        import getopt

        src = ""
        dst = ""

        try:
            opts, args = getopt.getopt(argv,"hi:o:s:d:",["src=", "dst=", "inputv=","outputv="])
        except getopt.GetoptError:
            print self.usage()
            sys.exit(2)

        for opt, arg in opts:
            if opt == '-h':
                print self.usage()
                sys.exit()
            elif opt in ("-s", "--src"):
                src = arg
                self.config.setDataPath(arg)
            elif opt in ("-d", "--dst"):
                dst = arg
                self.config.setOutputPath(arg)
            elif opt in ("-i", "--inputv"):
                if arg in self.config.getInputVersions():
                    self.config.setInputVersion(arg)
                else:
                    print "ERROR:", arg, "is not valid input version"
                    print self.usage()
                    sys.exit(1)
            elif opt in ("-o", "--outputv"):
                if arg in self.config.getOutputVersions():
                    self.config.setOutputVersion(arg)
                else:
                    print "ERROR:", arg, "is not valid output version"
                    print self.usage()
                    sys.exit(1)

        if not src or not dst:
            print "ERROR: scrapbookdata or destination is empty"
            print self.usage()
            sys.exit(1)

        print self.config.printConfiguration()

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    parser = ArgsParser()
    parser.parse(sys.argv[1:])
    ScrabDict().create(parser.config.getDataPath(), parser.config.getOutputPath()) # TODO just pass config
