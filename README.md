

 ### Script to transfer files with a simple copy/paste from terminal when no other options are available
 
* Yet another pentesting script

* It convert a target file to transfer in base64 rows and generates convenient output


```
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
```


Example:

```

./cpyvenom.py -p windows/powershell -i simpleapp.exe -d c:\\temp\\simpleapp.exe
Input file is  simpleapp.exe
Output file is StdOut
Payload  windows/powershell
Destination c:\temp\simpleapp.exe

Copy from here:

$FilePath="c:\temp\simpleapp.exe"
$EncodedString =  '' 
$EncodedString+="TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA4AAAAA4fug4AtAnNIbgB" 
$EncodedString+="TM0hVGhpcyBwcm9ncmFtIGNhbm5vdCBiZSBydW4gaW4gRE9TIG1vZGUuDQ0KJAAAAAAAAABMzsLOCK+snQivrJ0Ir6ydWsepnBCv" 
$EncodedString+="rJ1ax6icBa+snVrHrZwNr6ydHMStnAyvrJ0Ir62dWK+sna3GqZwJr6ydrcZTnQmvrJ2txq6cCa+snVJpY2gIr6ydAAAAAAAAAABQ" 
$EncodedString+="RQAATAEJAH3RQGAAAAAAAAAAAOAAAgELAQ4QAHIAAABKAAAAAAAAnRMBAAAQAAAAEAAAAABAAAAQAAAAAgAABgAAAAAAAAAGAAAA" 
$EncodedString+="AAAAAAAgAgAABAAAAAAAAAMAQIEAABAAABAAAAAAEAAAEAAAAAAAABAAAAAAAAAAAAAAACjSAQBkAAAAAAACADwEAAAAAAAAAAAA" 
$EncodedString+="AAAAAAAAAAAAABACACgEAAAApQEAOAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADilAQBAAAAAAAAAAAAAAAAA0AEAKAIAAAAA" 
            --- cut ----
$EncodedString+="cD94P5Q/nD/oP/Q/ALABABQAAABUMFgwdDB4MJQwmDAA8AEADAAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" 
$EncodedString+="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" 
$EncodedString+="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" 
$EncodedString+="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" 
$EncodedString+="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" 
$EncodedString+="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" 
$EncodedString+="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" 
$EncodedString+="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" 
$EncodedString+="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" 
$EncodedString+="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" 
$EncodedString+="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" 
$EncodedString+="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" 
$EncodedString+="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" 
$EncodedString+="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=" 
$ByteArray = [System.Convert]::FromBase64String($EncodedString);
[System.IO.File]::WriteAllBytes($FilePath, $ByteArray);

```







