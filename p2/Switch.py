# Project 2 for OMS6250
#
# This defines a Switch that can can send and receive spanning tree 
# messages to converge on a final loop free forwarding topology.  This
# class is a child class (specialization) of the StpSwitch class.  To 
# remain within the spirit of the project, the only inherited members
# functions the student is permitted to use are:
#
# self.switchID                   (the ID number of this switch object)
# self.links                      (the list of swtich IDs connected to this switch object)
# self.send_message(Message msg)  (Sends a Message object to another switch)
#
# Student code MUST use the send_message function to implement the algorithm - 
# a non-distributed algorithm will not receive credit.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2016 Michael Brown, updated by Kelly Parks
#           Based on prior work by Sean Donovan, 2015
			    												

from Message import *
from StpSwitch import *

class Switch(StpSwitch):
    def __init__(self, idNum, topolink, neighbors): 
        # Invoke the super class constructor, which makes available to this object the following members:
        # -self.switchID                   (the ID number of this switch object)
        # -self.links                      (the list of swtich IDs connected to this switch object)
        super(Switch, self).__init__(idNum, topolink, neighbors)
        #TODO: Define a data structure to keep track of which links are part of / not part of the spanning tree.
        self.root_switch_id = self.switchID
        self.distance_to_root = 0
        self.active_links = []
        self.switchThrough = self.switchID 

    def send_initial_messages(self):
        #TODO: This function needs to create and send the initial messages from this switch.
        #      Messages are sent via the superclass method send_message(Message msg) - see Message.py.
        #      Use self.send_message(msg) to send this.  DO NOT use self.topology.send_message(msg)
        for neighbor in self.links:
            message = Message(self.switchID,0,self.switchID, neighbor, False)
            self.send_message(message)
        return
    
    # Helper for sending messages to neighbors
    def determine_message_type_to_neighbors(self):
        for neighbor in self.links:
            message = Message(self.root_switch_id, self.distance_to_root, self.switchID,neighbor, self.switchThrough==neighbor)
            self.send_message(message)
        return
        
    def process_message(self, message):
        #TODO: This function needs to accept an incoming message and process it accordingly.
        #      This function is called every time the switch receives a new message.
        if message.pathThrough and message.origin not in self.active_links:
            self.active_links.append(message.origin)
        # if neither pass through each other
        elif not message.pathThrough and message.origin != self.switchThrough:
            if message.origin in self.active_links:
                self.active_links.remove(message.origin)

        if message.root < self.root_switch_id:
            self.root_switch_id = message.root
            self.distance_to_root = message.distance+1
            self.switchThrough = message.origin
            # append to active links
            if message.origin not in self.active_links:
                self.active_links.append(message.origin)

            self.determine_message_type_to_neighbors()

        elif message.root == self.root_switch_id:

            if message.distance+1 < self.distance_to_root:
                self.distance_to_root = message.distance+1
                self.active_links.remove(self.switchThrough)
                self.switchThrough = message.origin
                if message.origin not in self.active_links:
                    self.active_links.append(message.origin)
      
                self.determine_message_type_to_neighbors()

            elif message.distance+1 == self.distance_to_root:
                # compare origin ID with self.switchThrough
                if self.switchThrough > message.origin:
                    # remove switchThrough from AL
                    if self.switchThrough in self.active_links:
                        self.active_links.remove(self.switchThrough)
                    self.switchThrough = message.origin
                    if message.origin not in self.active_links:
                        self.active_links.append(message.origin)

                elif self.switchThrough < message.origin:
                    if message.origin in self.active_links:
                        self.active_links.remove(message.origin)

                self.determine_message_type_to_neighbors()

        return
        
    def generate_logstring(self):
        #TODO: This function needs to return a logstring for this particular switch.  The
        #      string represents the active forwarding links for this switch and is invoked 
        #      only after the simulaton is complete.  Output the links included in the 
        #      spanning tree by increasing destination switch ID on a single line. 
        #      Print links as '(source switch id) - (destination switch id)', separating links 
        #      with a comma - ','.  
        #
        #      For example, given a spanning tree (1 ----- 2 ----- 3), a correct output string 
        #      for switch 2 would have the following text:
        #      2 - 1, 2 - 3
        #      A full example of a valid output file is included (sample_output.txt) with the project skeleton.
        log_string =  ""
        for link in sorted(self.active_links):
            log_string += "%d - %d, " %(self.switchID, link)
        log_string = log_string[:-2]  
        return log_string
