"""
pyOpt_objective

Holds the Python Design Optimization Classes (base and inherited).

"""

__version__ = '$Revision: $'


#import os, sys
#import pdb

inf = 10.E+20  # define a value for infinity



class Objective(object):
    
    '''
    Optimization Objective Class
    '''
    
    def __init__(self, name, value=0.0, optimum=0.0):
        
        '''
        Objective Class Initialization
        
        **Arguments:**
        
        - name -> STR: Objective Group Name
        
        **Keyword arguments:**
        
        - value-> FLOAT: Initial objective value, *Default* = 0.0
        - optimum-> FLOAT: Optimum objective value, *Default* = 0.0
        
        Documentation last updated:  Feb. 07, 2011 - Peter W. Jansen
        '''
        
        # 
        self.name = name
        self.value = value
        self.optimum = optimum
        
        
    def ListAttributes(self):
        
        '''
        Print Structured Attributes List
        
        Documentation last updated:  March. 10, 2008 - Ruben E. Perez
        '''
        
        ListAttributes(self)
        
        
    def __str__(self):
        
        '''
        Structured Print of Objective
        
        Documentation last updated:  April. 30, 2008 - Peter W. Jansen
        '''
        
        return ( '        Name        Value        Optimum\n'+'	 '+str(self.name).center(9) +'%12g  %12g\n' %(self.value,self.optimum))
    


def ListAttributes(self):
        
        '''
        Print Structured Attributes List
        
        Documentation last updated:  March. 24, 2008 - Ruben E. Perez
        '''
        
        print('\n')
        print('Attributes List of: ' + repr(self.__dict__['name']) + ' - ' + self.__class__.__name__ + ' Instance\n')
        self_keys = self.__dict__.keys()
        self_keys.sort()
        for key in self_keys:
            if key != 'name':
                print(str(key) + ' : ' + repr(self.__dict__[key]))
        print('\n')
    



# Objective Test
if __name__ == '__main__':
    
    print('Testing ...')
    
    # Test Ojective
    obj = Objective('f')
    obj.ListAttributes()
    
