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
        tags = [x for x in self.__splitTags(keyval[1]) if x.startswith('#')]
        for tag in tags: # save available tags
            tagPair = ("tag", tag)
            pageInfo.append(tagPair)
        if len(tags) == 0: # if no tags present, move to tagless
            tagPair = ("tag", "#tagless")
            pageInfo.append(tagPair)
        print 'tags =', tags
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
