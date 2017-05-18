#!/bin/bash

# cd to script directory
function GoToScriptDirectory
{
    cd "${0%/*}"
}

function GoToProjectDirectory
{
    GoToScriptDirectory
    cd ".."
}

GoToProjectDirectory

#python ./traverse.py ../.
#python ./traverse.py /home/andrew/.mozilla/firefox/hfsek638.default/ScrapBook/data/
#python src/export.py /home/andrew/.mozilla/firefox/hfsek638.default/ScrapBook/data/ /tmp/ScrabDict.xml
python src/main.py -s /home/andrew/.mozilla/firefox/hfsek638.default/ScrapBook/data/ -d /tmp/ScrabDict.xml

