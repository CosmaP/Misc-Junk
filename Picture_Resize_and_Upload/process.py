#!/usr/bin/env python3

#======================================================================
#
#  Image Processor for Breuer-Weil
#  
#  V 0.1
#
#======================================================================

#======================================================================
# Start of Main Imports and setup constants

# Module Imports
import os, sys
#import Image
import argparse                   # Import Argument Parser
from PIL import Image
from resizeimage import resizeimage
import config

# Setup constants
size = 300, 300                   # Output Size
Hight = 300
Width = 300

# Folders
InputFolder = config.INFOLDER
OutputFolder = config.OUTFOLDER
ThumbnailsFolder = config.THUMBNAILS

# Web Storage Credentials
FTPServer = config.FTPSERVER
FTPPort = config.FTPPORT
FTPUserName = config.FTPUSERNAME
FTPPassword = config.FTPPASSWORD

# End of Main Imports and setup constants
#======================================================================

#======================================================================
# Initialisation procedures

# End of Initialisation procedures
#======================================================================

#======================================================================
# Service Procedures

# End of Service Procedures    
#======================================================================

#======================================================================
# Task Procedures

def imageResize01(inpath, outpath):
    
    file_dir=os.path.split(inpath)

    Files = os.listdir(inpath) # returns list

    for infile in Files:
        print ('***********************************************************************************')
        outfile = os.path.splitext(outpath)[0] + '/' + infile + '.thumbnail'
        infile = os.path.splitext(inpath)[0] + '/' + infile
        print('infile - ' + infile)
        print('outfile - ' + outfile)
        img = Image.open(infile)
        if infile != outfile:
            try:
                if img.size[0] > img.size[1]:
                    aspect = img.size[1]/120
                    new_size = (int(img.size[0])/aspect, 120)
                else:
                    aspect = img.size[0]/120
                    new_size = (120, int(img.size[1]/aspect)
                
                img.resize(new_size).save(file_dir[0] + '/ico' + file_dir[1][3:])
                img = Image.open(file_dir[0] + '/ico' + file_dir[1][3:])

                if img.size[0] > img.size[1]:
                    new_img = img.crop( (
                    (((img.size[0])-120)/2), 0,120+(((img.size[0])-120)/2),120 ) )
                else:
                    new_img = img.crop( (0,(((img.size[1])-120)/2),120,120+(((img.size[1])-120)/2)) )

                new_img.save(file_dir[0]+'/ico'+file_dir[1][3:])
            except IOError:
                print ("cannot create thumbnail for '%s'" % infile)


def imageResize02(inpath, outpath):

  print(inpath)
  for infile in inpath:
      print(infile)
      outfile = os.path.splitext(outpath)[0] + ".thumbnail"
      # print(outfile + '\n')
      if infile != outfile:
          try:
              im = Image.open(infile)
              im.thumbnail(size, Image.ANTIALIAS)
              im.save(outfile, "JPEG")
          except IOError:
            print ("cannot create thumbnail for '%s'" % infile)

def imageResize03(in_file, out_file, size):

    with open(in_file) as fd:
        image = resizeimage.resize_thumbnail(Image.open(fd), size)
    image.save(out_file)
    image.close()

def imageResize04(inpath, outpath):

    #Files = glob.glob(inpath)
    size = 300, 300
    
    Files = os.listdir(inpath) # returns list

    #print(Files)
    for infile in Files:
        print ('***********************************************************************************')
        print(infile)
        infile = os.path.splitext(inpath)[0] + '/' + infile
        outfile = os.path.splitext(outpath)[0] + '/' + infile + '.thumbnail'
        print(outfile)
        if infile != outfile:
            try:
                print ('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
                im = Image.open(infile)
                print ('yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')
                im.thumbnail(size, Image.ANTIALIAS)
                print ('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
                im.save(outfile, "JPEG")
                print ('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            except IOError:
                print ("cannot create thumbnail for '%s'" % infile)



# End of Task Procedures    
#======================================================================

#======================================================================            
# __Main__ Startup Loop        
       
if __name__ == '__main__': # The Program will start from here

    # Get and parse Arguments
    parser = argparse.ArgumentParser(description='Breuer-Weil Image Resizer and Uploader')
    parser.add_argument('-v',dest='height', type=int, help='Final Image Height')                                  # Final Image Height
    parser.add_argument('-l',dest='width', type=int, help='Final Image Height')                                   # Final Image Width
    parser.add_argument('-i',dest='inputlocation', type=str, help='Image Input Location')                         # Image Input Location
    parser.add_argument('-o',dest='outputlocation', type=str, help='Image Output Location')                       # Image Output Location
    parser.add_argument('-t',dest='thumbnails', type=str, help='Thumbnail Output Location')                       # Thumbnail Output Location
    parser.add_argument('-x',dest='testinfile', type=str, help='Test Input File')                                 # Test Input File
    parser.add_argument('-y',dest='testoutfile', type=str, help='Test Output File')                               # Test Output File
    parser.add_argument('-f',dest='ftpserver', type=str, help='FTP Server to send files to')                      # FTP Server to send files to
    parser.add_argument('-p',dest='ftpport', type=str, help='FTP Port to use')                                    # FTP Port to use
    parser.add_argument('-u',dest='ftpusername', type=str, help='FTP Username to use')                            # FTP Username to use
    parser.add_argument('-s',dest='ftppassword', type=str, help='FTP Password to use\n\n')                        # FTP Password to use
    args = parser.parse_args()
    
    if ((str(args.height)) != 'None'):
        print ('\nOutput Height - ',(str(args.height)))
        Height = int(args.height)

    if ((str(args.width)) != 'None'):
        print ('Output Width - ',(str(args.width)))
        Width = int(args.width)

    if ((str(args.inputlocation)) != 'None'):
        print ('\nInput Folder - ',(str(args.inputlocation)))
        InputFolder = args.inputlocation

    if ((str(args.outputlocation)) != 'None'):
        print ('\nOutput Folder - ',(str(args.Speed)))
        OutputFolder = args.outputlocation

    if ((str(args.thumbnails)) != 'None'):
        print ('\nThumbnails Folder - ',(str(args.thumbnails)))
        ThumbnailsFolder = args.thumbnails

    if ((str(args.testinfile)) != 'None'):
        print ('\nTest Input File - ',(str(args.testinfile)))
        TestInFile = args.testinfile

    if ((str(args.testoutfile)) != 'None'):
        print ('\nTest Output File - ',(str(args.testoutfile)))
        TestOutFile = args.testoutfile
    
    if ((str(args.ftpserver)) != 'None'):
        print ('\nFTP Server - ',(str(args.ftpserver)))
        FTPServer = args.ftpserver
 
    if ((str(args.ftpport)) != 'None'):
        print ('\nFTP Port - ',(str(args.ftpport)))
        FTPPort = int(args.ftpport)
    else:
        FTPPort = 21

    if ((str(args.ftpusername)) != 'None'):
        print ('\nFTP User Name - ',(str(args.ftpusername)))
        FTPUserName = args.ftpusername

    if ((str(args.ftppassword)) != 'None'):
        print ('\nFTP User Password - xxxxxxxxxxxxxxxxx')
        FTPPassword = args.ftppassword
    
        
    print ('\n\nSetting Up ...\n')
   
    print ('\nGo ...\n\n')

    # InputFolder = config.INFOLDER
    # OutputFolder = config.OUTFOLDER
    # ThumbnailsFolder = config.THUMBNAILS

    size = (256, 256)

    try:
        imageResize01(InputFolder, OutputFolder)
        #imageResize02(InputFolder, OutputFolder)
        #imageResize02(TestInFile, TestOutFile)
        #imageResize03(TestInFile, TestOutFile, size)
        #imageResize04(InputFolder, OutputFolder)
        print ('\n\n................... Exit .......................\n\n')
        exit(0) # Exit Cleanly
    except KeyboardInterrupt:
        print ('\n\n................... Exit .......................\n\n')
        exit(0) # Exit Cleanly
        
# End of __Main__ Startup Loop 
#======================================================================