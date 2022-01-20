# Project 4 for CS 6250: Computer Networks
#
# This defines a DistanceVector (specialization of the Node class)
# that can run the Bellman-Ford algorithm. The TODOs are all related 
# to implementing BF. Students should modify this file as necessary,
# guided by the TODO comments and the assignment instructions. This 
# is the only file that needs to be modified to complete the project.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2017 Michael D. Brown
# Based on prior work by Dave Lillethun, Sean Donovan, and Jeffrey Randow.
        											
from Node import *
from helpers import *

class DistanceVector(Node):
    
    def __init__(self, name, topolink, outgoing_links, incoming_links):
        ''' Constructor. This is run once when the DistanceVector object is
        created at the beginning of the simulation. Initializing data structure(s)
        specific to a DV node is done here.'''

        super(DistanceVector, self).__init__(name, topolink, outgoing_links, incoming_links)
        self.dv = {name: 0}
        #TODO: Create any necessary data structure(s) to contain the Node's internal state / distance vector data    
    

    def send_initial_messages(self):
        ''' This is run once at the beginning of the simulation, after all
        DistanceVector objects are created and their links to each other are
        established, but before any of the rest of the simulation begins. You
        can have nodes send out their initial DV advertisements here. 

        Remember that links points to a list of Neighbor data structure.  Access
        the elements with .name or .weight '''

        # TODO - Each node needs to build a message and send it to each of its neighbors
        # HINT: Take a look at the skeleton methods provided for you in Node.py
        self.message_helper()


    def process_BF(self):
        ''' This is run continuously (repeatedly) during the simulation. DV
        messages from other nodes are received here, processed, and any new DV
        messages that need to be sent to other nodes as a result are sent. '''

        # Implement the Bellman-Ford algorithm here.  It must accomplish two tasks below:
        # 1. Process queued messages       
        dv_updated = False
        for msg in self.messages:  
            for node in msg["dv"].keys():

                if node == self.name:
                    continue
                
                if node not in self.dv:
                    if self.outgoing_neighbor(node):
                        weight = int(self.get_outgoing_neighbor_weight(node))
                    else:
                        weight = int(msg["dv"][node]) + int(self.get_outgoing_neighbor_weight(msg["origin"]))
                    self.dv[node] = weight
                    dv_updated = True
                
                else:
                    origin_dst = int(self.get_outgoing_neighbor_weight(msg["origin"]))
                    node_dst = int(msg["dv"][node])
                    updated_dst = node_dst + origin_dst 
                    # handle -99 checks prior to update
                    if origin_dst <= -99 or node_dst <= -99 or updated_dst <= -99:
                        if self.dv[node] != -99:
                            self.dv[node] = -99
                            dv_updated = True
                    else:
                        if updated_dst > -99 and updated_dst < self.dv[node]:
                            self.dv[node] = updated_dst
                            dv_updated = True
        
        # Empty queue
        self.messages = []

        #2. Send neighbors updated distances 
        if dv_updated:
            self.message_helper()              

    def outgoing_neighbor(self, node):
        for link in self.outgoing_links:
            if link == node:
                return True
        return False

    def message_helper(self):
        for link in self.incoming_links:
            message = { "origin": self.name, "dv": self.dv.copy(), "dest": link }
            self.send_msg(message, link.name)

    def log_distances(self):
        ''' This function is called immedately after process_BF each round.  It 
        prints distances to the console and the log file in the following format (no whitespace either end):
        
        A:A0,B1,C2
        
        Where:
        A is the node currently doing the logging (self),
        B and C are neighbors, with vector weights 1 and 2 respectively
        NOTE: A0 shows that the distance to self is 0 '''
        distances = []
        comma = ","
        for node in self.dv:
            distances.append(node + str(self.dv[node]))
        distances.sort()
        # TODO: Use the provided helper function add_entry() to accomplish this task (see helpers.py).
        # An example call that which prints the format example text above (hardcoded) is provided.        
        add_entry(self.name, comma.join(distances))        
