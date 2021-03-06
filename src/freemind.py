import os
from traverse import TraverseScrabBook
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
import datetime

class FreeMind:

    # id start
    __id    = 100000000
    # positions for uber node (child of center node)
    __right = 'right'
    __left  = 'left'
    # colors
    __black  = '#000000'
    __blue   = '#000066'
    __orange = '#cc6600'
    #limits
    __desertLimit   = 3
    __popularLimit  = 7

    #def __init__(self, path):
    #    self.path = path

    def __setCenter(self, root, text):
        root = self.__addVersion(root)
        return self.__addTextNode(root, text)

    def __setUberNode(self, center, position, text, color, folded = False):
        uber = self.__addFoldedLocation(center, position) if folded else self.__addLocation(center, position)
        self.__addNodeProperty(uber, text, color)
        self.__setNodeBold(uber)
        return uber

    def __setTagNode(self, parent, text, color):
        tag = self.__addFoldedNode(parent)
        self.__addNodeProperty(tag, text, color)
        self.__setNodeBold(tag)
        return tag

    def __fillTags(self, center, text, position, dictionary, minLimit, maxLimit, folded = False):
        node = self.__setUberNode(center, position, text, self.__orange, folded)
        for tag,pages in dictionary.tagPages().iteritems():
            if len(pages) > minLimit and len(pages) <= maxLimit:
                tag = self.__setTagNode(node, tag, self.__blue)
                self.__fillTagExtensions(tag, pages)
        return node

    def __fillByDate(self, center, text, position, dictionary, folded = False, dayLimit = ""):
        node = self.__setUberNode(center, position, text, self.__orange, folded)
        for date,pages in dictionary.datePages().iteritems():
            if not dayLimit or date > dayLimit:
                tag = self.__setTagNode(node, date, self.__blue)
                self.__fillTagExtensions(tag, pages)
        return node

    def __isExtensions(self, page):
        return (len(page.pdfs) > 0)

    def __fillTagExtensions(self, parent, pages):
        for page in pages:
            titlelink = self.__addFoldedLink(parent, page.title, page.link)

            # make title bold if extensions present
            if (self.__isExtensions(page)):
                self.__setNodeBold(titlelink)

            # add index file link
            self.__addLink(titlelink, "index", page.indexPath)

            # add source link
            self.__addLink(titlelink, "source", page.source)

            # add pdfs if present
            if (len(page.pdfs) > 0):
                pdfs = self.__addFoldedNode(titlelink)
                self.__addNodeProperty(pdfs, "pdfs", self.__black)
                for pdf in page.pdfs:
                    self.__addLink(pdfs, pdf.title, pdf.link)
        return parent

    def __fillTagsDesert(self, center, dictionary):
        folded = True
        return self.__fillTags(center, '#TagsDesert', self.__left, dictionary, 0, 3, folded)

    def __fillRecent(self, center, dictionary):
        notFolded = False
        dateLimit = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y%m%d')
        return self.__fillByDate(center, '#Recent', self.__left, dictionary, notFolded, dateLimit)

    def __fillHistory(self, center, dictionary):
        folded = True
        return self.__fillByDate(center, '#ByDate', self.__left, dictionary, folded)

    def __fillTagsPopular(self, center, dictionary):
        return self.__fillTags(center, '#Popular', self.__right, dictionary, 3, 7)

    def __fillTagsEpics(self, center, dictionary):
        return self.__fillTags(center, '#Epics', self.__right, dictionary, 7, 99999)

    def __fillTagless(self, center, dictionary):
        folded = True
        node = self.__setUberNode(center, self.__right, '#Tagless', self.__orange, folded)
        for tag,pages in dictionary.tagPages().iteritems():
            if tag == '#tagless':
                self.__fillTagExtensions(node, pages)
        return node

    def create(self, path, dictionary):
        root        = Element('map')
        center      = self.__setCenter(root, 'ScrabDic')

        self.__fillTagsDesert(center, dictionary)
        self.__fillTagsPopular(center, dictionary)
        self.__fillTagsEpics(center, dictionary)
        self.__fillTagless(center, dictionary)
        self.__fillRecent(center, dictionary)
        self.__fillHistory(center, dictionary)

        if not path:
            print self.__prettify(root)  # FIXME remove
        else:
            # write to file
            with open(path, 'w') as fmFile:
                fmFile.write(self.__prettify(root).split('\n', 1)[-1])

        return True

    def __prettify(self, elem):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = tostring(elem, 'utf-8', method="xml")
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def __addVersion(self, root):
        root.set('version', '0.9.0') # freemind .mm version supported
        root.append(Comment('To view this file, download free mind mapping software FreeMind from http://freemind.sourceforge.net'))
        return root

    def __addNode(self, parent):
        self.__id += 1
        return SubElement(parent, 'node', {
            'CREATED':'1493235457878', # TODO get some true value
            'ID':str(self.__id),
            'MODIFIED':'1493235457879', # TODO get some true value
            })

    def __addFoldedNode(self, parent):
        self.__id += 1
        return SubElement(parent, 'node', {
            'CREATED':'1493235457878', # TODO get some true value
            'FOLDED':'true',
            'ID':str(self.__id),
            'MODIFIED':'1493235457879', # TODO get some true value
            })


    def __addTextNode(self, parent, text):
        self.__id += 1
        return SubElement(parent, 'node', {
            'CREATED':'1493235457878', # TODO get some true value
            'ID':str(self.__id),
            'MODIFIED':'1493235457879', # TODO get some true value
            'TEXT':text,
            })

    def __addFoldedLink(self, parent, text, link):
        self.__id += 1
        return SubElement(parent, 'node', {
            'CREATED':'1493235457878', # TODO get some true value
            'ID':str(self.__id),
            'FOLDED':'true',
            'LINK':link,
            'MODIFIED':'1493235457879', # TODO get some true value
            'TEXT':text,
            })

    def __addLink(self, parent, text, link):
        self.__id += 1
        return SubElement(parent, 'node', {
            'CREATED':'1493235457878', # TODO get some true value
            'ID':str(self.__id),
            'LINK':link,
            'MODIFIED':'1493235457879', # TODO get some true value
            'TEXT':text,
            })

    def __addLocation(self, parent, position):
        self.__id += 1
        return SubElement(parent, 'node', {
            'CREATED':'1493235457878', # TODO get some true value
            'ID':str(self.__id),
            'MODIFIED':'1493235457879', # TODO get some true value
            'POSITION':position,
            })

    def __addFoldedLocation(self, parent, position):
        self.__id += 1
        return SubElement(parent, 'node', {
            'CREATED':'1493235457878', # TODO get some true value
            'ID':str(self.__id),
            'FOLDED':'true',
            'MODIFIED':'1493235457879', # TODO get some true value
            'POSITION':position,
            })

    def __setNodeBold(self, target):
        return SubElement(target, 'font', {
            'BOLD':'true',
            'NAME':'SansSerif',
            'SIZE':'12',
            })

    def __addNodeProperty(self, parent, text, color):
        node = SubElement(parent, 'richcontent', {
            'TYPE':'NODE',
            })
        html = SubElement(node, 'html')
        head = SubElement(html, 'head')
        head.text = '    '
        body = SubElement(html, 'body')
        p    = SubElement(body, 'p')
        font = SubElement(p, 'font', {
            'color':color,
            })
        font.text = text
        return node

    # add unpopulat tags
    def __fillUnpopular(self, parent):
        parent

if __name__ == "__main__":
    import sys
    print "Hello!"
    #print( FreeMind().create() )
