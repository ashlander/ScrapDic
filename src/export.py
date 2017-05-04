import os
#from os import listdir, walk
#from os.path import isfile, join, getsize
from traverse import TraverseScrabBook
from tagdictionary import TagDictionary
from freemind import FreeMind

class ScrabDict:

    #def __init__(self, path):
    #    self.path = path

    def __splitLine(self, line):
        return line.translate(None, '\n').split("\t", 1)

    def __splitTags(self, line):
        return line.split(" __BR__ ", len(line))

    def __parseComment(self, comment):
        pageInfo = list()
        keyval = self.__splitLine(comment)
        tags = self.__splitTags(keyval[1])
        for tag in tags:
            if tag.startswith("#"):
                tagPair = ("tag", tag)
                pageInfo.append(tagPair)
        return pageInfo

    def __parseIndex(self, data):
        pageInfo = list()
        for record in data:
            if record.find("comment") == 0:
                pageInfo += self.__parseComment(record)
            else:
                pageInfo.append( self.__splitLine(record) )

        # parsed index list output
        for pair in pageInfo:
            print "\t", pair[0], '\t\t', pair[1]

        return pageInfo

    def create(self, srcPath, dstPath):
        # reading information of ScrabBook
        scrabBook = TraverseScrabBook().withPath(srcPath)
        dictionary = TagDictionary()
        for scrabPage in scrabBook:
            srcPath = scrabPage[0]
            metaData = scrabPage[1]
            files = scrabPage[2]

            print "[INF] Parsing index file ", srcPath, ""
            pageInfo = self.__parseIndex(metaData)

            print "[INF] Generating tags dictionary"
            dictionary.addPage(pageInfo, srcPath, files)

            #break # FIXME remove

        print "[INF] Serializing to freemind"
        FreeMind().create(dstPath, dictionary)

        return True

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    print( ScrabDict().create(sys.argv[1], sys.argv[2]) )
