#!/usr/bin/env python3

#======================================================================
#
#  Image Processor for Breuer-Weil
#  
#  V 0.1
#
#=====================================================================

#======================================================================
# Start of Main Imports and setup constants

# Module Imports
import os, sys, time
import subprocess
from pathlib import Path
import argparse                   # Import Argument Parser
from PIL import Image
import config
from time import gmtime, strftime
import ftplib

# Setup constants
size = config.SIZE                  # Output Size

# Folders
InputFolder = config.INFOLDER
OutputFolder = config.OUTFOLDER
ThumbnailsFolder = config.THUMBNAILS
RejectsFolder = config.REJECTSFOLDER
LogFolder = config.LOGFOLDER

# Web Storage Credentials
FTPServer = config.FTPSERVER
FTPPort = config.FTPPORT
FTPFolder = config.FTPFOLDER
FTPUserName = config.FTPUSERNAME
FTPPassword = config.FTPPASSWORD

# End of Main Imports and setup constants
#======================================================================

#======================================================================
# Initialisation Procedures

def cleanuplogs(logfolder):

    now = time.time()

    for f in os.listdir(logfolder):
        f = logfolder + '/' + f
        if os.stat(f).st_mtime < now -2 * 86400:
            if os.path.isfile(f):
                os.remove(f)

def setuprunlog(runlog):
    today = strftime("%Y-%m-%d", gmtime())
    
    runlog = runlog + '/' + today + '-Run.log'
        
    RunLog = open(runlog,"a+")
    print ('\n................... RunLog Opened ......................')

    return(RunLog)

def setuperrorlog(errorlog):
    today = strftime("%Y-%m-%d", gmtime())
    
    errorlog = errorlog + '/' + today + '-Error.log'
    
    ErrorLog = open(errorlog,"a+")
    print ('\n................... ErrorLog Opened ....................')
    
    return(ErrorLog)
   
# End of Initialisation Procedures
#======================================================================

#======================================================================
# Service Procedures

def logging(LogFile, Type, Message):

    #today = strftime("%Y-%m-%d", gmtime())
    now = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    if Type=='E':
        LogFile.write(now + Message)
    elif Type=='R':
        LogFile.write(now + Message)

def ftpfiletoserver(outname, outpath, ErrorLog, RunLog, ftp, FTPFolder):
    
    #ftp.set_debuglevel(2)
    #ftp.cwd(FTPFolder)
    os.chdir(outpath)

    logging(RunLog, 'R', ' Upload Output File  - ' + outname + '\n')

    #file = open(outname, 'rb')                  # file to send
    #cmd = 'STOR ' + outname
    #ftp.storbinary(cmd, file)     # send the file

    cmd = 'sudo cp "' + outname + '" "' + ftp + FTPFolder + '/' + outname + '"'

    # print (cmd)

    status = subprocess.call(cmd, shell=True) 
    # print (status)

    if status == 0:
        os.remove(outname)
        logging(RunLog, 'R', ' Removed Output File - ' + outname + '\n')
    else:
        logging(RunLog, 'E', ' File Error, No Copy - ' + outname + '\n')
        logging(RunLog, 'R', ' File Error, No Copy - ' + outname + '\n')

    os.chdir('..')

def RejectFile(infile, outname, RejectsFolder, ErrorLog, RunLog):

    outfile = RejectsFolder + "/" + outname
    print('Rejected File \t- ' + outfile)
    logging(RunLog, 'R', ' Move Rejected File  - ' + infile + '\n')
    os.rename(infile, outfile)
    logging(RunLog, 'R', ' Moved Rejected File - ' + outfile + '\n')
    
# End of Service Procedures    
#======================================================================

#======================================================================
# Task Procedures

def imageResize(inpath, outpath, size, ErrorLog, RunLog, ftp, FTPFolder):

    Files = os.listdir(inpath) # returns list
    count = 0
   
    #print(Files)
    for infile in Files:
        count = count + 1
        print (str(count) + '\t ***********************************************')
        logging(RunLog, 'R', ' ' + str(count) + '\t ******************************************************************************\n')
        outname = infile
        outfile = os.path.splitext(outpath)[0] + '/' + infile
        infile = os.path.splitext(inpath)[0] + '/' + infile
        filetype = os.path.splitext(infile)[1]
        
        print('File Type\t- ' + filetype)
        print('Input File\t- ' + infile)
        print('Output File\t- ' + outfile)

        logging(RunLog, 'R', ' File Type\t\t\t- ' + filetype + '\n')
        logging(RunLog, 'R', ' Input File\t\t\t- ' + infile + '\n')
        logging(RunLog, 'R', ' Output File\t\t\t- ' + outfile + '\n')

        if filetype == '.jpg' or filetype == '.JPG' or filetype == '.JEPG' or filetype == '.jpeg':
            if infile != outfile:
                try:
                    im = Image.open(infile)
                    im.thumbnail(size, Image.ANTIALIAS)
                    im.save(outfile, "JPEG")
                    ftpfiletoserver(outname, outpath, ErrorLog, RunLog, ftp, FTPFolder)
                    print("Uploaded \t- %s" % outfile)
                    logging(RunLog, 'R', " Uploaded \t\t\t- %s\n" % outfile)
                    os.remove(infile)
                    logging(RunLog, 'R', ' Removed Input File\t- ' + infile + '\n')
                except IOError:
                    print ("Cannot process %s - %s. Please Review." % (infile, outfile))
                    logging(RunLog, 'R', " Cannot process %s - %s. Please Review.\n" % (infile, outfile))
                    logging(ErrorLog, 'E', " Cannot process %s - %s. Please Review.\n" % (infile, outfile))
        elif filetype == '.gif' or filetype == '.GIF':
            if infile != outfile:
                try:
                    im = Image.open(infile)
                    im.thumbnail(size, Image.ANTIALIAS)
                    rgb_im = im.convert('RGB')
                    outfile = outfile + '.jpg'
                    rgb_im.save(outfile)
                    ftpfiletoserver(outname + '.jpg', outpath, ErrorLog, RunLog, ftp, FTPFolder)
                    print("Uploaded  \t- %s" % outfile)
                    logging(RunLog, 'R', " Uploaded  \t\t\t- %s\n" % outfile)
                    os.remove(infile)
                    logging(RunLog, 'R', ' Removed Input File\t- ' + infile + '\n')
                except IOError:
                    print ("Cannot process %s - %s. Please Review." % (infile, outfile))
                    logging(RunLog, 'R', " Cannot process %s - %s. Please Review.\n" % (infile, outfile))
                    logging(ErrorLog, 'E', " Cannot process %s - %s. Please Review.\n" % (infile, outfile))
        elif filetype == '.png' or filetype == '.PNG':
            if infile != outfile:
                try:
                    im = Image.open(infile)
                    im.thumbnail(size, Image.ANTIALIAS)
                    rgb_im = im.convert('RGB')
                    outfile = outfile + '.jpg'
                    rgb_im.save(outfile)
                    ftpfiletoserver(outname + '.jpg', outpath, ErrorLog, RunLog, ftp, FTPFolder)
                    print("Uploaded \t- %s" % outfile)
                    logging(RunLog, 'R', " Uploaded  \t\t\t- %s\n" % outfile)
                    os.remove(infile)
                    logging(RunLog, 'R', ' Removed Input File\t- ' + infile + '\n')
                except IOError:
                    print ("Cannot process %s - %s. Please Review." % (infile, outfile))
                    logging(RunLog, 'R', " Cannot process %s - %s. Please Review.\n" % (infile, outfile))
                    logging(ErrorLog, 'E', " Cannot process %s - %s. Please Review.\n" % (infile, outfile))
        elif filetype == '.bmp' or filetype == '.BMP':
            if infile != outfile:
                try:
                    im = Image.open(infile)
                    im.thumbnail(size, Image.ANTIALIAS)
                    rgb_im = im.convert('RGB')
                    outfile = outfile + '.jpg'
                    rgb_im.save(outfile)
                    ftpfiletoserver(outname + '.jpg', outpath, ErrorLog, RunLog, ftp, FTPFolder)
                    print("Uploaded \t- %s" % outfile)
                    logging(RunLog, 'R', " Uploaded  \t\t\t- %s\n" % outfile)
                    os.remove(infile)
                    logging(RunLog, 'R', ' Removed Input File\t- ' + infile + '\n')
                except IOError:
                    print ("Cannot process %s - %s. Please Review." % (infile, outfile))
                    logging(RunLog, 'R', " Cannot process %s - %s. Please Review.\n" % (infile, outfile))
                    logging(ErrorLog, 'E', " Cannot process %s - %s. Please Review.\n" % (infile, outfile))
        else:
            RejectFile(infile, outname, RejectsFolder, ErrorLog, RunLog)
            print('\n********************************** Not Processed **********************************\n')
            logging(RunLog, 'R', ' File Rejected \t\t- ' + infile + '\n')
            logging(RunLog, 'R', ' ********************************** Not Processed **********************************\n')
            logging(ErrorLog, 'E', ' ' + infile + ' moved to Reject folder\n')
            logging(ErrorLog, 'E', ' ********************************** Not Processed **********************************\n')
            

        # EndIf
    print('\t ***********************************************')
    logging(RunLog, 'R', ' ***********************************************************************************\n')



# End of Task Procedures    
#======================================================================

#======================================================================
# Shutdown Procedures

def cleanup(RunLog, ErrorLog, FTP):

    #FTP.quit()
    print ('\n................... FTP Closed .........................')
    RunLog.close()
    print ('\n................... RunLog Closed ......................')
    ErrorLog.close()
    print ('\n................... ErrorLog Closed ....................\n\n')
    
    
# End of Shutdown Procedures
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
        
    print ('\n................... Setting Up .........................')

    today = strftime("%Y-%m-%d", gmtime())
    now = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    print ('\n................... Clean-up Logs ......................')
    cleanuplogs(LogFolder)

    print ('\n................... Open RunLog ........................')
    RunLog = setuprunlog(LogFolder)
    
    print ('\n................... Open ErrorLog ......................')
    ErrorLog = setuperrorlog(LogFolder)
    
    print ('\n................... Setup FTP Connection ...............')
    logging(RunLog, 'R', ' ....................... Setup FTP Connection ......................................\n')
                           
    #ftp = ftplib.FTP(FTPServer, FTPUserName, FTPPassword)
    ftp = '/var/www/html/'
    print ('\n................... FTP Connection Setup ...............')
    #ftp.login()

    print ('\n................... Start Run ..........................\n\n')
    now = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    logging(RunLog, 'R', ' ....................... Run Started ' + now + ' ...........................\n')
    logging(ErrorLog, 'E', ' ....................... Run Started ' + now + '  ...........................\n')
   
    try:
        imageResize(InputFolder, OutputFolder, size, ErrorLog, RunLog, ftp, FTPFolder)
        print ('\n\n................... Run Finished .......................')
        now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        logging(RunLog, 'R', ' ....................... Run Finished ' + now + ' ...........................\n\n')
        logging(ErrorLog, 'E', ' ....................... Run Finished ' + now + ' ...........................\n\n')
        print('\n................... Shutting Down ......................')
        cleanup(ErrorLog, RunLog, ftp)
        exit(0) # Exit Cleanly
    except KeyboardInterrupt:
        print ('\n\n................... Run Aborted ........................')
        now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        logging(RunLog, 'R', ' ....................... Run Aborted  ' + now + ' ...........................\n\n')
        logging(ErrorLog, 'E', ' ....................... Run Aborted  ' + now + ' ...........................\n\n')
        print('\n................... Shutting Down ......................\n')
        cleanup(ErrorLog, RunLog, ftp)
        exit(0) # Exit Cleanly
        
# End of __Main__ Startup Loop 
#======================================================================