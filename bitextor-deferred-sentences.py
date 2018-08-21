import sys
from wagnerfischer import WagnerFischer
import base64
import html5lib
from lxml import etree

documentStandoff = dict()
with open(sys.argv[1],'r') as reader:
    for line in reader:
        fields = line.split('\t')
        fields = list(map(str.strip, fields))
        document = html5lib.parse(base64.b64decode(fields[0]),treebuilder="lxml",namespaceHTMLElements=False)
        documentStandoff[fields[1]]=(document,fields[4].split(';'))

for line in sys.stdin:
    fields = line.split('\t')
    fields = list(map(str.strip, fields)) #Strip all elements

    shortpathSL=WagnerFischer(fields[2].split(' '),str(etree.tostring(documentStandoff[fields[0]][0], encoding='utf8', method="text")).split()).optimum_alignments() #Calculate a short distance path using Wagner-Fischer algorightm for source
    shortpathTL=WagnerFischer(fields[3].split(' '),str(etree.tostring(documentStandoff[fields[1]][0], encoding='utf8', method="text")).split()).optimum_alignments() #and target sentences
    
    position=0
    standoffSL=[]
    for op in shortpathSL: #Obtain the standoff annotation of each sentence word from the full annotated document they come from, counting non-inserted words
        if op != "I":
            standoffSL.append(documentStandoff[fields[0]][1][position])
        position = position + 1
    fields.append(";".join(standoffSL))
    
    position=0
    standoffTL=[]
    for op in shortpathTL:
        if op != "I":
            standoffTL.append(documentStandoff[fields[1]][1][position])
        position = position + 1
    fields.append(";".join(standoffTL))

    #TODO: simplify the sentence standoff annotation joining/collapsing word standoff annotations with the same tag path

    print("\t".join(fields))
