#!/usr/bin/env python3

import sys, getopt
from base64 import b64encode
import datetime


def usage():
    print ("""

..######..########..##....##.##.....##.########.##....##..#######..##.....##
.##....##.##.....##..##..##..##.....##.##.......###...##.##.....##.###...###
.##.......##.....##...####...##.....##.##.......####..##.##.....##.####.####
.##.......########.....##....##.....##.######...##.##.##.##.....##.##.###.##
.##.......##...........##.....##...##..##.......##..####.##.....##.##.....##
.##....##.##...........##......##.##...##.......##...###.##.....##.##.....##
..######..##...........##.......###....########.##....##..#######..##.....##

    
Transfer files with a simple copy/paste from terminal when no other options are available


Usage: cpyvenom.py -p <payload> -i <inputfile> -d <destination> -o <save_to_outputfile> -b 100 

Available commands:

    -p / --payload          windows/powershell, windows/certutil, linux/bash, linux/python

    -i / --input-file       file path to send

    -o / --output-file      save output to file, default to stdout

    -d / --destination      destination path in the remote system

    -b / --block            size of the block

    Example:

        windows:
            cpyvenom -i nc.exe -o nc.cpyvenom -p winows/powershell -d "C:\\\\temp"

        linux:
            cpyvenom -i /bin/nc -o nc.cpv -p linux/bash -d /tmp/nc





""")



def cpyvenom(inputfile,outputfile,payload,destination,block):
    try:
        f = open(inputfile,'rb')
        content = f.read()

        text = ""

        if not payload:
            payload = "windows/powershell"

        if payload.lower() == "windows/powershell":
            text = """\nCopy from here:\n\n$FilePath="{}"\n$EncodedString =  '' \n""".format(destination)
            encoded = b64encode(content).decode('ascii')
            splitted_encoded = [encoded[i:i+block] for i in range(0, len(encoded), block)]
            for s in splitted_encoded:
                text += """$EncodedString+="{0}" \n""".format(s)
            text += """$ByteArray = [System.Convert]::FromBase64String($EncodedString);\n[System.IO.File]::WriteAllBytes($FilePath, $ByteArray);\n"""
            if not outputfile:
                print (text)
            
        
        if payload.lower()=="windows/certutil":
            suffix = datetime.datetime.now().strftime("%y%m%d%H%M%S")
            basename = "b64_"+suffix
            text = """\nCopy from here:\n\n"""
            encoded = b64encode(content).decode('ascii')
            splitted_encoded = [encoded[i:i+block] for i in range(0, len(encoded), block)]
            for s in splitted_encoded:
                text += """echo {0} >> %Temp%\\{1}\n""".format(s,basename)
            text += """certutil -decode %Temp%\\{0} {1}\n""".format(basename,destination)
            if not outputfile:
                print (text)


        if payload.lower()=="linux/bash":
            suffix = datetime.datetime.now().strftime("%y%m%d%H%M%S")
            basename = ".b64_"+suffix
            text = """\nCopy from here:\n\n"""
            encoded = b64encode(content).decode('ascii')
            splitted_encoded = [encoded[i:i+block] for i in range(0, len(encoded), block)]
            for s in splitted_encoded:
                text += """echo {0} >> /tmp/{1}\n""".format(s,basename)
            text += """base64 -d /tmp/{0} > {1}\nrm -f /tmp/{0}""".format(basename,destination)
            if not outputfile:
                print (text)


        if payload.lower()=="linux/python":
            text = """\nCopy from here:\n\nfrom base64 import b64decode\ns=""\n"""
            encoded = b64encode(content).decode('ascii')
            splitted_encoded = [encoded[i:i+block] for i in range(0, len(encoded), block)]
            for s in splitted_encoded:
                text += """s+="{0}"\n""".format(s)
            text += """decoded = b64decode(s)\n"""
            text += """f = open("{0}", 'wb')\nf.write(decoded)\nf.close()\n""".format(destination)


            if not outputfile:
                print (text)
            else:
                try:
                    f = open(destination,'w')
                    f.write(text)
                    f.close()
                    print("\nGenerated file{0}\n ".format(destination))
                except IOError:
                    print("Output file not accessibile")
                    exit(0)


        # Do something with the file
    except IOError:
        print("File not accessible")
        exit(0)
    finally:
        f.close()




def main(argv):
    inputfile = ''
    outputfile = ''
    payload = ''
    destination = ''
    block = 100
    
    try:
       opts, args = getopt.getopt(argv,"hp:i:o:f:d:b:",["payload=","input-file=","output-file=","destination-file=","block="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    if len(opts)==0:
        usage()
        exit(0)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-i", "--input-file"):
            inputfile = arg
        elif opt in ("-o", "--output-file"):
            outputfile = arg
        elif opt in ("-p","--payload"):
            payload = arg
        elif opt in ("-d","--destination-file"):
            destination = arg
        elif opt in ("-b","--block"):
            block = int(arg)   

    print ("Input file is ", inputfile)
    print ("Output file is ", 'StdOut' if not outputfile else outputfile) # if no output, default to stdout
    print ("Payload ", payload)   # default to windows/powershell
    print ("Destination" , destination)   
    

    if not inputfile or not destination:
        usage()
        exit(0)

    cpyvenom(inputfile,outputfile,payload,destination,block)

if __name__ == "__main__":
   main(sys.argv[1:])