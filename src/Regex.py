from dataclasses import dataclass
from typing import Union as TypingUnion
from .NFA import NFA

EPSILON = ''  # Epsilon transition representation

class Regex:
    def thompson(self) -> NFA[int]:
        raise NotImplementedError("Subclasses must implement the thompson method.")

@dataclass
class Character(Regex):
    char: str

    def thompson(self) -> NFA[int]:
        start_state = 0
        accept_state = 1
        S = {self.char}
        K = {start_state, accept_state}
        q0 = start_state
        d={}
        d[(start_state, self.char)] = {accept_state}
        F = {accept_state}
        return NFA(S, K, q0, d, F)

@dataclass
class Concat(Regex):
    left: Regex
    right: Regex

    def thompson(self) -> NFA[int]:
        left1 = self.left.thompson()
        right1 = self.right.thompson()

        S = left1.S | right1.S
        K = set()
        q0 = left1.q0
        d = {}
        F = set()



        left_state = {}
        for state in left1.K:
            left_state[state] = state
        right_state={}
        for state in right1.K:
            right_state[state] = state + max(left1.K) + 1
     

        for state in left_state.values():
            K.add(state)
        for state in right_state.values():
            K.add(state)

        for (from_state, symbol), to_states in left1.d.items():
            for to_state in to_states:
                d[(left_state[from_state], symbol)] = {left_state[to_state]}


        for (from_state, symbol), to_states in right1.d.items():
            for to_state in to_states:
                d[(right_state[from_state], symbol)] = {right_state[to_state]}

    
        for accept in left1.F:
            d[(left_state[accept], EPSILON)] = {right_state[right1.q0]}

        q0 = left_state[left1.q0]

        for accept in right1.F:
            F.add(right_state[accept])

        return NFA(S, K, q0, d, F)



@dataclass
class Union(Regex):
    left: Regex
    right: Regex

    def thompson(self) -> NFA[int]:
        left1 = self.left.thompson()
        right1 = self.right.thompson()

        K = set()
        d = {}
        F = set()
        S = left1.S | right1.S
        q0 = 0


        final_state = max(left1.K) + max(right1.K) + 3
        F.add(final_state)

        K.add(q0)
        K.add(final_state)

        left_state = {}
        for state in left1.K:
            left_state[state] = state + 1

        right_state = {}
        for state in right1.K:
            right_state[state] = state + max(left1.K) + 2

        for state in left_state.values():
            K.add(state)

        for state in right_state.values():
            K.add(state)

        for (from_state, symbol), to_states in left1.d.items():
            for to_state in to_states:
                d[(left_state[from_state], symbol)] = {left_state[to_state]}


        for (from_state, symbol), to_states in right1.d.items():
            for to_state in to_states:
                d[(right_state[from_state], symbol)] = {right_state[to_state]}
      
        d[(q0, EPSILON)] = {left_state[left1.q0], right_state[right1.q0]}

        for accept_state in left1.F:
          d[(left_state[accept_state], EPSILON)] = {final_state}
        for accept_state in right1.F:
            d[(right_state[accept_state], EPSILON)] = {final_state}

        return NFA(S, K, q0, d, F)

@dataclass
class Question_Mark(Regex):

    regex: Regex

    def thompson(self) -> NFA[int]:
        base = self.regex.thompson()

        K = set()
        d = {}
        F = set()
        S = base.S

        state1 = {}
        for state in base.K:
            state1[state] = state + 1

        for state in state1.values():
            K.add(state)

        for (from_state, symbol), to_states in base.d.items():
            for to_state in to_states:
                d[(state1[from_state], symbol)] = {state1[to_state]}

        start_state = 0
        accept_state = max(base.K) + 2
        K.add(start_state)
        K.add(accept_state)


        for accept in base.F:
            d[(state1[accept], EPSILON)] = {accept_state}
     
        d[(start_state, EPSILON)] = {state1[base.q0], accept_state}

        q0 = start_state
        F.add(accept_state)

        return NFA(S, K, q0, d, F)


@dataclass
class Plus(Regex):
    regex: Regex

    def thompson(self) -> NFA[int]:
        base = self.regex.thompson()

        K = set()
        d = {}
        F = set()
        S = base.S

        state1 = {}
        for state in base.K:
            state1[state] = state + 1

        for state in state1.values():
            K.add(state)

        for (from_state, symbol), to_states in base.d.items():
            for to_state in to_states:
                d[(state1[from_state], symbol)] = {state1[to_state]}

        start_state = 0
        accept_state = max(base.K) + 2
        K.add(start_state)
        K.add(accept_state)

        d[(start_state, EPSILON)] = {state1[base.q0]}

        for accept in base.F:
            d[(state1[accept], EPSILON)] = {state1[base.q0]}


        for accept in base.F:
            d[(state1[accept], EPSILON)] = {accept_state}

        q0 = start_state
        F.add(accept_state)

        return NFA(S, K, q0, d, F)

@dataclass
class CharacterClass(Regex):
    def __init__(self, start_char: str, end_char: str):
        self.start_char = start_char
        self.end_char = end_char

    def thompson(self) -> NFA[int]:
        start_state = 0
        accept_state = 1
        S = set()
        for i in range(ord(self.start_char), ord(self.end_char) + 1):
            S.add(chr(i))
        K = {start_state, accept_state}
        q0 = start_state
        d = {}
        F = {accept_state}
        for char in range(ord(self.start_char), ord(self.end_char) + 1):
            d[(start_state, chr(char))] = {accept_state}

        return NFA(S, K, q0, d, F)

@dataclass
class Star(Regex):
    regex: Regex
    def thompson(self) -> NFA[int]:
        base = self.regex.thompson()


        K = set()
        d = {}
        F = set()
        S = base.S

        state1={}
        for state in base.K:
            state1[state] = state + 1
   
        for state in state1.values():
            K.add(state)

        for (from_state, symbol), to_states in base.d.items():
            for to_state in to_states:
                d[(state1[from_state], symbol)] = {state1[to_state]}


        start_state = 0
        accept_state = max(base.K) + 2
        K.add(start_state)
        K.add(accept_state)

      
        d[(start_state, EPSILON)] = {state1[base.q0], accept_state}

        for accept in base.F:
      
            d[(state1[accept], EPSILON)] = {state1[base.q0], accept_state}

        q0 = start_state
        F.add(accept_state)

        return NFA(S, K, q0, d, F)


def parse_regex(regex: str) -> Regex:
    stack = []
    i = 0
    while i < len(regex):
        char = regex[i]

        if char == ' ':
            i += 1
            continue

        elif char == '(':
            count = 1
            start = i + 1
            i += 1
            while count > 0 and i < len(regex):
                if regex[i] == '(':
                    count += 1
                elif regex[i] == ')':
                    count -= 1
                i += 1
            sub_regex = parse_regex(regex[start: i - 1])
            stack.append(sub_regex)
        elif char == '\\':
            if i + 1 < len(regex):
                if regex[i + 1] == ' ':
                    stack.append(Character(' '))
                elif regex[i + 1] == '(':
                    stack.append(Character('('))
                    i += 1
                elif regex[i + 1] == ')':
                    stack.append(Character(')'))
                    i += 1
                elif regex[i + 1] == '+':
                    stack.append(Character('+'))
                    i += 1
                elif regex[i + 1] == '*':
                    stack.append(Character('*'))
                    i += 1
                elif regex[i + 1] == '/':
                    stack.append(Character('/'))
                    i += 1

            i += 1

        elif char == '\n':
            stack.append(Character('\n'))
            i += 1

        elif char.isalnum() or char == '.' or char == '-' or char == ':' or char == '_' or char == '@': 
            stack.append(Character(char))
            i += 1

        elif char == '[':
            i += 1
            a1 = regex[i]
            i += 2
            a2 = regex[i]
            i += 2
            stack.append(CharacterClass(a1, a2))
                 
        elif char == '+':
            expr = stack.pop()
            stack.append(Plus(expr))
            i += 1

        elif char == '*':

            expr = stack.pop()
            stack.append(Star(expr))
            i += 1
        
        elif char == '?':
            expr = stack.pop()
            stack.append(Question_Mark(expr))
            i += 1

        elif char == '|':
            right_expr = regex[i+1:]
            left_expr = regex[0:i]
            stack.clear()
            left_regex = parse_regex(left_expr)
            right_regex = parse_regex(right_expr)
            stack.append(Union(left_regex, right_regex))
            break

    while len(stack) > 1:
        right = stack.pop()
        left = stack.pop()
        stack.append(Concat(left, right))
    return stack[0]
