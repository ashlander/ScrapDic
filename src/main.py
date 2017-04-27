from export import ScrabDict

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    print( ScrabDict().create(sys.argv[1], sys.argv[2]) )
