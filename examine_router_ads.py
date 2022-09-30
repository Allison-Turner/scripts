#! /usr/bin/env python3
import pyshark

FILE1 = "/home/allison/Desktop/router-ground-truthing/pcaps/router-discovery-2022-08-12-17-24-55-cogsci-002.pcapng"
FILE2 = "/home/allison/Desktop/router-ground-truthing/pcaps/router-discovery-2022-08-12-17-40-13-student-center-b.pcapng"
FILE3 = "/home/allison/Desktop/router-ground-truthing/pcaps/router-discovery-2022-08-12-17-52-11-taco-villa.pcapng"
FILE4 = "/home/allison/Desktop/router-ground-truthing/pcaps/router-discovery-2022-08-12-17-59-32-tata-hall.pcapng"
FILE5 = "/home/allison/Desktop/router-ground-truthing/pcaps/router-discovery-2022-08-15-10-13-29-cse-building.pcapng"


def examine_ndp_ras(f):

    capture = pyshark.FileCapture(f)
    
    prefixes = []

    for p in capture:
        if(p.__contains__("icmpv6")):
            if int(p.icmpv6.get_field_value("type")) == 134:
                #print(dir(p.icmpv6))
                pfix = p.icmpv6.get_field_value("opt_prefix")
                
                if pfix not in prefixes:
                	prefixes.append(pfix) 

                
    print(prefixes)
    
print(FILE1)        
examine_ndp_ras(FILE1)
print(FILE2)
examine_ndp_ras(FILE2)
print(FILE3)
examine_ndp_ras(FILE3)
print(FILE4)
examine_ndp_ras(FILE4)
print(FILE5)
examine_ndp_ras(FILE5)
