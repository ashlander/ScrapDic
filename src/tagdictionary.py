import os
import collections
from os.path import join, basename
from traverse import TraverseScrabBook

class TagLink:

    def __init__(self, title, link, indexPath, pdfs):
        self.title      = title
        self.link       = link
        self.indexPath  = indexPath
        self.pdfs       = pdfs

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

    def addPage(self, pageInfo, dirPath, indexPath, files):
        title = next((x[1] for x in pageInfo if x[0] == "title"), ["Unknown Title"])
        tags = [x[1] for x in pageInfo if x[0] == "tag"]

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

        tagLink = TagLink(title, link, indexPath, pdfs)

        for tag in tags:
            if self.__dictionary.has_key(tag):
                self.__dictionary[tag].append(tagLink)
            else:
                self.__dictionary[tag] = [tagLink]

        return True

    def tagPages(self):
        return  collections.OrderedDict(sorted(self.__dictionary.items()))

if __name__ == "__main__":
    import sys
    print "Hello!"
    #print( FreeMind().create() )
