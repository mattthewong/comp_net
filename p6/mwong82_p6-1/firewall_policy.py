#!/usr/bin/python
# CS 6250 Fall 2020 - SDN Firewall Project
# build anorak-v13

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import packets
from pyretic.core import packet

def determineProtocolNumber(inputType, num):
    if inputType == 'T':
        return packet.TCP_PROTO
    elif inputType == 'U':
        return packet.UDP_PROTO
    elif inputType == 'I':
        return packet.ICMP_PROTO
    else:
        return int(num)

def isEmptyEntry(entry):
    if entry['protocol'] != '-':
        return False
    elif entry['macaddr_src'] != '-':
        return False
    elif entry['macaddr_dst'] != '-':
        return False
    elif entry['ipaddr_src'] != '-':
        return False
    elif entry['ipaddr_dst'] != '-':
        return False
    elif entry['port_src'] != '-':
        return False
    elif entry['port_dst'] != '-':
        return False
    else:
        return True

def make_firewall_policy(config):

    # You may place any user-defined functions in this space.
    # You are not required to use this space - it is available if needed.

    # feel free to remove the following "print config" line once you no longer need it
    # it will not affect the performance of the autograder
    print config

    # The rules list contains all of the individual rule entries.
    disallowedrules = []

    for entry in config:
        # TODO - This is where you build your firewall implementation using the Pyretic Language
        # "config" is a list that contains all of the entries that are parsed from your firewall-config.pol file.
        # Each entry represents one line from the firewall-config.pol file.  The entry is a python dictionary that
        # contains each item defined in a single line from the firewall-config.pol file.  For instance, to access 
        # the source IP address, you will access the dictionary by using entry[ipaddr_src].  The name of each
        # dictionary item is defined in firewall.py

        # You will need to remove the line below and create an implementation that builds a pyretic firewall rules 
        # using the data passed in entry.  Refer to Pyretic Documentation to learn how to write this implementation.
        # (Hint:  What are you doing to the traffic?  Think about matching items in the headers)
        if isEmptyEntry(entry):
            continue
        else:
            rule = match()

            if entry['protocol'] != '-':
                rule &= match(protocol=determineProtocolNumber(entry['protocol'], entry['ipproto']))
                rule &= match(ethtype=packet.IPV4)
            if entry['macaddr_src'] != '-':
                rule &= match(srcmac=EthAddr(entry['macaddr_src']))
            
            if entry['macaddr_dst'] != '-':
                rule &= match(dstmac=EthAddr(entry['macaddr_dst']))
            
            if entry['ipaddr_src'] != '-':
                rule &= match(srcip=entry['ipaddr_src'])
            
            if entry['ipaddr_dst'] != '-':
                rule &= match(dstip=entry['ipaddr_dst'])
            
            if entry['port_src'] != '-':
                rule &= match(srcport=int(entry['port_src']))

            if entry['port_dst'] != '-':
                rule &= match(dstport=int(entry['port_dst']))

            disallowedrules.append(rule)
            pass

    # DO NOT EDIT BELOW THIS LINE.  Think about the following line.  What is it doing?  What happens if you remove the ~

    allowed = ~(union(disallowedrules))

    return allowed
