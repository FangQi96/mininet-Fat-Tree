#!/usr/bin/python
'''
Created on Nov 29, 2013

@author: farshad tajedin
'''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller , RemoteController,OVSSwitch

from optparse import OptionParser
from mininet.log import setLogLevel
from mininet.cli import CLI

class SingleSwitchTopo(Topo):
    def __init__(self, n=2, **opts):
        Topo.__init__(self, **opts)
        self.args=None
        self.options=None
        self.parseArgs()
        self.TotalLink=0
        self.dpid=0
        #k=self.options.kterm
        self.Host=[]
        self.CoreSwitch=[]
        self.AggregationSwitch=[]
        self.EdgeSwitch=[]
        #thread.start_new_thread(function, args)
        self.addEdgeSwitches()
        self.addAggregationSwitches()
        self.addCoreSwitches()
        self.addHosts()
        self.addLinks()
       
    def addCoreSwitches(self):
        k=self.options.kterm
        for x in range(0,(k/2)**2):
            self.CoreSwitch.append(self.addSwitch( 'C_S'+str(x),dpid='0001'+self.convertToDPIDformat() ))
            self.dpid+=1
        self.dpid=0
    
    def addAggregationSwitches(self):
        k=self.options.kterm
        for x in range(0, k*k/2):
            self.AggregationSwitch.append(self.addSwitch( 'A_S'+str(x),dpid='0002'+self.convertToDPIDformat() ))
            self.dpid+=1
        self.dpid=0
             
    def addEdgeSwitches(self):
        k=self.options.kterm
        for x in range(0, k*k/2):
            self.EdgeSwitch.append(self.addSwitch( 'E_S'+str(x),dpid='0003'+self.convertToDPIDformat()  ))
            self.dpid+=1
        self.dpid=0
    #dpid='0003'+'{0:048b}'.format(self.dpid)    
    def addHosts(self):
        k=self.options.kterm
        for x in range(0,(k**3)/4):
            self.Host.append(self.addHost( 'H'+str(x) ))
     
    def addLinks(self):
        k=self.options.kterm  
        
        #connecting Edge switches to hosts 
        for x in range(0,k*k/2):
            for y in range(0,k/2):
                self.addLink( self.EdgeSwitch[x], self.Host[y+(k/2)*x],y )
                #self.addLink(node1, node2, port1, port2)
                self.TotalLink+=1
                
        #thread.start_new_thread(function, args)
        for x in range(0,k):
            for y in range(0,k/2):
                for z in range(0,k/2):
                    #connecting Aggregation switches to Edge switches 
                    self.addLink( self.AggregationSwitch[y+(k/2)*x], self.EdgeSwitch[z+(k/2)*x],z,k/2+y )
                    self.TotalLink+=1
                    #connecting Core switches to Aggregation switches 
                    self.addLink( self.CoreSwitch[z+(y*k/2)], self.AggregationSwitch[x*(k/2)+y],x,k/2+z )
                    self.TotalLink+=1
                       
    def parseArgs( self ):
        opts = OptionParser()
        opts.add_option("--kterm",type='int' ,default=4, help="K term for FatTree Topology")
        (self.options, self.args) = opts.parse_args()       
     
    def convertToDPIDformat(self):
        paddTo12=''    
        temp=12-len(hex(self.dpid)[2:])
        for i in range(0,temp):
            paddTo12+= '0'
        return paddTo12+hex(self.dpid)[2:]
         


def simpleTest():
    "Create and test a simple network"
    topo = SingleSwitchTopo()
    hst=[]
    net = Mininet( topo=topo,switch=OVSSwitch, controller=lambda name: RemoteController( name, ip='127.0.0.1' ) )
    c0 = RemoteController( 'c0', ip='127.0.0.1' )
    net.start()
    c0.start()
    hosts=topo.Host
    
    print "total links is: %s" %(topo.TotalLink) 
    
    for i in range(0,len(hosts)):
        hst.append(net.get('H'+str(i)))

    CLI(net)
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()    
