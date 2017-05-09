from os import listdir, walk
from os.path import isfile, join, getsize

class ScrabPage:

    def __init__(self, pathDir, indexFile, indexData, listFiles):
        self.pathDir   = pathDir
        self.indexFile = indexFile
        self.indexData = indexData
        self.listFiles = listFiles

    def __repr__(self):
        return "( dir = " + self.pathIndex + ", index = " + self.link + ", \n\tfiles = " + self.listFiles + ")"

class TraverseScrabBook:

    __scrabBookIndex = "index.dat"

    def __getDirs(self, path):
        return walk(path).next()[1]

    # return list of tuples containing (directory path, index file data, list of files inside)
    def withPath(self, path):
        scrabInfo = list()

        for dirName in self.__getDirs(path):

            dirPath = join(path, dirName)
            print "[INF] Found", dirPath

            onlyfiles = [f for f in listdir(dirPath) if isfile(join(dirPath, f))]

            # retrieving index file
            if self.__scrabBookIndex in onlyfiles:
                indexFile = join(dirPath, self.__scrabBookIndex)
                try:
                    with open (indexFile, "r") as index:
                        data = index.readlines()
                        scrabInfo.append( ScrabPage(dirPath, self.__scrabBookIndex, data, onlyfiles))
                except:
                    print "[WARN] skipping file", indexFile, "because of error"

        return scrabInfo

if __name__ == "__main__":
    import sys
    print( TraverseScrabBook().withPath(sys.argv[1]) )
