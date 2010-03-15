'''
Created on 12/03/2010

@author: Ezequiel
'''
import unittest
import caexplosion

test_nodes={'A': (1.5,1.5),
            'B':(1.5,2.5),
            'C': (2.5,1.5),
            'D': (2.5,2.5)}
test_connections=[('A', 'B'),('B', 'D'),('C','A'),('D','C')]
con_param_labels=('connection_area','permeability')
connection_parameters=[(1.0,0.1),(2.0,0.5),(1.5,4.2)]
default_connection_parameters=(1.0,1.0)

def distance(a,b):
    '''Returns the distance between a and b'''
    from math import sqrt
    return sqrt((a[0]-b[0])**2, (a[1]-b[1])**2)
    
class SimpleMeshCreationTestCase(unittest.TestCase):
    def setUp(self):
        '''
        Grafo: A, B, C, D      
        A: ubicado en (1.5, 1.5)      
        B: ubicado en (1.5, 2.5)      
        C: ubicado en (2.5, 1.5)      
        D: ubicado en (2.5, 2.5)       
        Conexiones: 
        A<->B 
        A<->C  
        C<->D  
        B<->D
        ''' 
        self.exp_subs=caexplosion.CAExplosion()
    def tearDown(self):
        self.exp_subs=None
        
    def testCreateEmptyMesh(self):
        self.mesh=self.exp_subs.Mesh()
        self.assertEqual(self.mesh.size(),0)
        
    def testBuildNodes(self):
        #Builds nodes
        for tag, pos in test_nodes.iteritems():
            new_node=self.mesh.Node()
            returned_tag=self.mesh.add(tag, new_node, pos)
            self.assertEqual(returned_tag, tag)
            self.assertEqual(self.mesh.get_position(tag), pos)
            
        
        self.assertEqual(self.mesh.order(), len(test_nodes))
        
    def testRepeatedTags(self):
        #Checks that nodes can't have the same tag
        for tag, pos in test_nodes.iteritems():
            new_node=self.mesh.Node()
            self.assertRaises(caexplosion.ExistingNodeError, self.mesh.add, args=(tag, new_node, pos) )
        
        #checks no new node was added
        self.assertEqual(self.mesh.size(), len(test_nodes))
            
    def testConnectNodesUsingTags(self):
        connect_iter=iter(test_connections)
        def_params=dict(zip(con_param_labels, default_connection_parameters))
                        
        for param in connection_parameters:
            connect=connect_iter.next()
            kwparam=dict(zip(con_param_labels, param))
            edge=self.mesh.connect(*connect, **kwparam)
            d=distance(test_nodes[connect[0]], test_nodes[connect[1]])
            self.assertAlmostEqual(edge.length, d, 5)
            
            #test given parameters are correctly set
            for key, value in kwparam.iteritems():
                self.assertEqual(edge.__dict__[key], value)
            
        #Set remaining connections assuming default parameters
        for connect in connect_iter:
            edge=self.mesh.connect(*connect)
            
            d=distance(test_nodes[connect[0]], test_nodes[connect[1]])
            self.assertAlmostEqual(edge.length, d, 5) 
            #test default parameters are correctly set
            kwparam=dict(zip(con_param_labels, default_connection_parameters))
            for key, value in kwparam.iteritems():
                self.assertEqual(edge.__dict__[key], value)
            
            
        self.assertEqual(self.mesh.size(), len(test_connections))
        
    def testRepeatedEdges(self):
        for connection in test_connections:
            #We can't add the same connection again
            self.assertRaises(caexplosion.ExistingEdgeError, self.mesh.connect, args=(connection[0], connection[1]))
            #We can't add the transposed connection because it is undirected graph
            self.assertRaises(caexplosion.ExistingEdgeError, self.mesh.connect, args=(connection[1], connection[0]))
            
        #No edge was added
        self.assertEqual(self.mesh.size(), len(test_connections))

    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()