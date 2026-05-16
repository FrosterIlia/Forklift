from abc import ABC, abstractmethod
from typing import Optional, List

class State(ABC):
    def __init__(self, sm: 'HierarchicalStateMachine') -> None:
        self._sm: 'HierarchicalStateMachine' = sm
        self._parent: Optional['State'] = None
        self._default_substate: Optional['State'] = None

    def set_parent(self, parent: 'State') -> None:
        self._parent = parent

    def set_default_sub_state(self, substate: 'State') -> None:
        self._default_substate = substate

    def get_parent(self) -> Optional['State']:
        return self._parent

    def onEnter(self) -> None:
        pass

    @abstractmethod
    def onRun(self) -> None:
        pass

    def onExit(self) -> None:
        pass


class HierarchicalStateMachine:
    def __init__(self) -> None:
        self._transition_pending: bool = False
        self._current_state: Optional[State] = None
        self._next_state: Optional[State] = None

    def initialize(self, initial_state: State) -> None:
        self._current_state = initial_state

        # Drill down to the default substate if the initial state is a composite
        while self._current_state and self._current_state._default_substate:
            self._current_state = self._current_state._default_substate

        # Enter the full path from root to current
        self._enter_path(self._current_state)

    def update(self) -> None:
        if self._transition_pending:
            self._execute_transition()
            self._transition_pending = False

        path: List[State] = []
        curr = self._current_state

        # Collect path up to Oldest Parent dynamically
        while curr:
            path.append(curr)
            curr = curr.get_parent()

        # Execute from Oldest Parent down to Youngest Child
        for state in reversed(path):
            state.onRun()

            # In case parent calls a state change, this prevents children from being executed.
            # In case there is a "stop" condition in the parent, children should not execute.
            if self._transition_pending:
                return

    def change_state(self, target_state: Optional[State]) -> None:
        if target_state:
            self._next_state = target_state
            self._transition_pending = True

    def is_in_state(self, state: State) -> bool:
        curr = self._current_state
        while curr:
            if curr is state:
                return True
            curr = curr.get_parent()
        return False

    def _execute_transition(self) -> None:
        if self._next_state is self._current_state:
            # Self-transition: Exit and Re-enter
            if self._current_state:
                self._current_state.onExit()
                self._current_state.onEnter()
            return

        # Find Least Common Ancestor
        lca = self._find_lca(self._current_state, self._next_state)

        # Exit from Current up to LCA
        curr = self._current_state
        while curr is not lca and curr is not None:
            curr.onExit()
            curr = curr.get_parent()

        # Drill down into target
        effective_target = self._next_state
        while effective_target and effective_target._default_substate:
            effective_target = effective_target._default_substate

        # Enter from LCA down to Effective Target
        entry_path: List[State] = []
        curr = effective_target
        
        while curr is not lca and curr is not None:
            entry_path.append(curr)
            curr = curr.get_parent()

        # Execute entries in reverse order (Top -> Down)
        for state in reversed(entry_path):
            state.onEnter()

        self._current_state = effective_target

    def _find_lca(self, source: Optional[State], target: Optional[State]) -> Optional[State]:
        s = source
        while s:
            t = target
            while t:
                if s is t:
                    return s
                t = t.get_parent()
            s = s.get_parent()
        return None

    def _enter_path(self, target: Optional[State]) -> None:
        """Helper for initialization"""
        path: List[State] = []
        curr = target
        
        while curr:
            path.append(curr)
            curr = curr.get_parent()
            
        for state in reversed(path):
            state.onEnter()