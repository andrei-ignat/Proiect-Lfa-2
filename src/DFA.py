from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar

STATE = TypeVar('STATE')

@dataclass
class DFA[STATE]:
    S: set[str]
    K: set[STATE]
    q0: STATE
    d: dict[tuple[STATE, str], STATE]
    F: set[STATE]
    

   

    def accept(self, word: str) -> bool:

        s = self.q0

        for ch in word:
            if (s,ch) in self.d:
                s = self.d(s,ch)
        
        if s in self.F:
            return True
        else:
            return False


    def remap_states[OTHER_STATE](self, f: Callable[[STATE], 'OTHER_STATE']) -> 'DFA[OTHER_STATE]':
      
        pass
    
    
    