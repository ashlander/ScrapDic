import os
import collections
from os.path import join, basename
from traverse import TraverseScrabBook

class TagLink:

    def __init__(self, title, link, indexPath, pdfs, source, datetime):
        self.title      = title # page title
        self.link       = link # link to localy saved path
        self.indexPath  = indexPath # path to index file
        self.pdfs       = pdfs # list of found pdf files
        self.source     = source # source site link
        self.datetime   = datetime # datetime as string YYYYMMDDhhmmss

    def __repr__(self):
        return "(" + self.title + "," + self.link + "," + self.indexPath + ")"

class PdfLink:

    def __init__(self, title, link):
        self.title      = title
        self.link       = link

    def __repr__(self):
        return "(" + self.title + "," + self.link + ")"

class TagDictionary:

    __scrabBookHtml = "index.html"

    def __init__(self):
        self.__dictionary = dict()
        self.__history    = dict()

    def addPage(self, pageInfo, dirPath, indexPath, files):
        title  = next((x[1] for x in pageInfo if x[0] == "title"), ["Unknown Title"])
        source = next((x[1] for x in pageInfo if x[0] == "source"), ["Unknown Source"])
        datetime = next((x[1] for x in pageInfo if x[0] == "id"), ["19700101000000"])
        tags   = [x[1] for x in pageInfo if x[0] == "tag"]

        # detecting link path if available
        link = ""
        if self.__scrabBookHtml in files:
            link = join(dirPath, self.__scrabBookHtml)

        # filter pdf files
        pdfs = list()
        pdfExt = ".pdf"
        for someFile in files:
            if (someFile.find(pdfExt, max(len(someFile)-len(pdfExt),0), len(someFile)) > 0):
                pdfs.append( PdfLink(someFile, join(dirPath,someFile)) )

        # remember parsed data, vital for processing
        tagLink = TagLink(title, link, indexPath, pdfs, source, datetime)

        # fill dictionary with tag -> pages
        for tag in tags:
            if self.__dictionary.has_key(tag):
                self.__dictionary[tag].append(tagLink)
            else:
                self.__dictionary[tag] = [tagLink]

        # fill dictionary with datetime -> page
        date = datetime[0:8]
        if self.__history.has_key(date):
            self.__history[date].append(tagLink)
        else:
            self.__history[date] = [tagLink]

        return True

    def tagPages(self):
        return collections.OrderedDict(sorted(self.__dictionary.items()))

    def datePages(self):
        return collections.OrderedDict(sorted(self.__history.items()))

if __name__ == "__main__":
    import sys
    print "Hello!"
    #print( FreeMind().create() )
