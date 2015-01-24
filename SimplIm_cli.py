#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image
import os, sys, getopt

def main(argv):
    largeur = 0
    hauteur = 0
    inputfile = ''
    output_file = 'resize'
    ratio_b  = False 
    qualityValue = 85
    format_output  = 'jpeg'
    howto = 'test.py -i photo -l <largeur> -h <hauteur> -q qualité -r -f format -o nom_de_sortie'

    try:
        opts, args = getopt.getopt(argv,"i:l:h:rq:o:f:",["ifile=","ofile="])
    except getopt.GetoptError:
       print  howto
       sys.exit(2)

    if len(opts) < 2:
        print howto
        sys.exit(1)

    for opt, arg in opts:
        if opt in ("-i"):
            inputfile = arg
            output_file = os.path.splitext(arg)[0] + '_resized'
        elif opt in ("-l"):
            largeur = int(arg)
        elif opt in ("-h" ):
            hauteur = int(arg)
        elif opt in ("-r"):
            ratio_b = True
        elif opt in ("-o"):
            output_file = arg
        elif opt in ("-q"):
            quality = int(arg)
        elif opt in ("-f"):
            format_output = arg

    try:
       im = Image.open(inputfile)
       ratio = float(im.size[0]) / im.size[1]
       miniature = im.thumbnail([128,128], Image.ANTIALIAS)
       if ratio_b == True: 
            if largeur != 0:
                hauteur = int (largeur / ratio)   
            elif hauteur != 0:
                largeur = int (hauteur * ratio)   
            else:
                hauteur = im.size[1]
                largeur = im.size[0]

       out = im.resize((hauteur,largeur))
       output_file = output_file+'.'+format_output
       print(inputfile + ' ' + str(im.size[1]) + 'x' + str(im.size[1]) + ' to ' + str(largeur) + 'x' + str(largeur) + ' saved in '+ output_file)
#optimize=True, progressive=True
       out.save(output_file, format_output, quality = qualityValue )
    except IOError:
        print("Error")
        pass


if __name__ == "__main__":
    main(sys.argv[1:])
