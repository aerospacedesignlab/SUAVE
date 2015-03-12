
# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# python imports
import numpy as np
from copy import deepcopy

# SUAVE imports
from SUAVE.Core                    import Data, Data_Exception
from SUAVE.Methods.Utilities            import atleast_2d_col

from Conditions import Conditions
from Unknowns   import Unknowns
from Residuals  import Residuals
from Numerics   import Numerics

import SUAVE
array_type = SUAVE.Plugins.VyPy.tools.arrays.array_type

# ----------------------------------------------------------------------
#  State
# ----------------------------------------------------------------------

class State(Conditions):
    
    def __defaults__(self):
        
        self.unknowns   = Unknowns()
        
        self.conditions = Conditions()
        
        self.residuals  = Residuals()
        
        self.numerics   = Numerics()
        
        self.initials   = Conditions()
        
        
    def expand_rows(self,rows):
        
        # store
        self._size = rows
        
        for k,v in self.iteritems():
            
            # don't expand initials or numerics
            if k in ('initials','numerics'):
                continue
            
            # recursion
            elif isinstance(v,Conditions):
                v.expand_rows(rows)
            # need arrays here
            elif np.rank(v) == 2:
                self[k] = np.resize(v,[rows,v.shape[1]])
            #: if type
        #: for each key,value        
        
        
        
class Container(State):
    def __defaults__(self):
        self.segments = Conditions()
        
    def merged(self):
        
        state_out = State()
        
        for i,(tag,sub_state) in enumerate(self.segments.items()):
            for key in ['unknowns','conditions','residuals']:
                if i == 0:
                    state_out[key].update(sub_state[key])
                else:
                    state_out[key] = state_out[key].do_recursive(append_array,sub_state[key])
            
        return state_out
        
State.Container = Container


def append_array(A,B=None):
    if isinstance(A,array_type) and isinstance(B,array_type):
        return np.vstack([A,B])
    else:
        return None