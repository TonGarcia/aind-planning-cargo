from aimacode.logic import PropKB
from aimacode.planning import Action
from aimacode.search import (
    Node, Problem,
)
from aimacode.utils import expr
from lp_utils import (
    FluentState, encode_state, decode_state,
)
from my_planning_graph import PlanningGraph

from functools import lru_cache


class AirCargoProblem(Problem):
    def __init__(self, cargos, planes, airports, initial: FluentState, goal: list):
        """
        :param cargos: list of str
            cargos in the problem
        :param planes: list of str
            planes in the problem
        :param airports: list of str
            airports in the problem
        :param initial: FluentState object
            positive and negative literal fluents (as expr) describing initial state
        :param goal: list of expr
            literal fluents required for goal test
        """
        self.state_map = initial.pos + initial.neg
        self.initial_state_TF = encode_state(initial, self.state_map)
        Problem.__init__(self, self.initial_state_TF, goal=goal)
        self.cargos = cargos
        self.planes = planes
        self.airports = airports
        self.actions_list = self.get_actions()

    def get_actions(self):
        """
        This method creates concrete actions (no variables) for all actions in the problem
        domain action schema and turns them into complete Action objects as defined in the
        aimacode.planning module. It is computationally expensive to call this method directly;
        however, it is called in the constructor and the results cached in the `actions_list` property.

        Returns:
        ----------
        list<Action>
            list of Action objects
        """

        # DONE: create concrete Action objects based on the domain action schema for: Load, Unload, and Fly
        # concrete actions definition: specific literal action that does not include variables as with the schema
        # for example, the action schema 'Load(c, p, a)' can represent the concrete actions 'Load(C1, P1, SFO)'
        # or 'Load(C2, P2, JFK)'.  The actions for the planning problem must be concrete because the problems in
        # forward search and Planning Graphs must use Propositional Logic

        def load_actions():
            """Create all concrete Load actions and return a list
            :return: list of Action objects
            """

            # Expected: Load(C1(cargo), P1(plane), SFO(airport))
            loads = []

            for cargo in self.cargos:
                for plane in self.planes:
                    for airport in self.airports:
                        # Use this to describe actions in PDDL
                        # action is an Expr where variables are given as arguments(args)
                        # Precondition and effect are both lists with positive and negated literals
                        pre_condition_negative = []
                        pre_condition_positive = [
                            expr("At({}, {})".format(cargo, airport)),
                            expr("At({}, {})".format(plane, airport))
                        ]

                        # incoming cargo
                        effect_add = [expr("In({}, {})".format(cargo, plane))]
                        # outgoing cargo
                        effect_rem = [expr("At({}, {})".format(cargo, airport))]

                        # Action builder: Load(C2, P2, JFK)
                        load = Action(
                            expr("Load({}, {}, {})".format(cargo, plane, airport)),
                            [pre_condition_positive, pre_condition_negative],
                            [effect_add, effect_rem]
                        )

                        # append load action
                        loads.append(load)

            # DONE: create all load ground actions from the domain Load action
            return loads

        def unload_actions():
            """Create all concrete Unload actions and return a list
            :return: list of Action objects
            """
            unloads = []

            for cargo in self.cargos:
                for plane in self.planes:
                    for airport in self.airports:
                        # Reverse what is plane At the airport & what cargo is in the plane
                        pre_condition_negative = []
                        pre_condition_positive = [
                            expr("In({}, {})".format(cargo, plane)),
                            expr("At({}, {})".format(plane, airport))
                        ]

                        # reverse outgoing cargo
                        effect_add = [expr("At({}, {})".format(cargo, airport))]
                        # reverse incoming cargo
                        effect_rem = [expr("In({}, {})".format(cargo, plane))]

                        # Build the Action the "get out" the cargo, using Unload(C2, P2, JFK)
                        unload = Action(
                            expr("Unload({}, {}, {})".format(cargo, plane, airport)),
                            [pre_condition_positive, pre_condition_negative],
                            [effect_add, effect_rem]
                        )

                        # append unload action
                        unloads.append(unload)

            # DONE: create all Unload ground actions from the domain Unload action
            return unloads

        def fly_actions():
            """Create all concrete Fly actions and return a list

            :return: list of Action objects
            """
            flys = []
            for fr in self.airports:
                for to in self.airports:
                    if fr != to:
                        for p in self.planes:
                            precond_pos = [expr("At({}, {})".format(p, fr))]
                            precond_neg = []
                            effect_add = [expr("At({}, {})".format(p, to))]
                            effect_rem = [expr("At({}, {})".format(p, fr))]
                            fly = Action(expr("Fly({}, {}, {})".format(p, fr, to)),
                                         [precond_pos, precond_neg],
                                         [effect_add, effect_rem])
                            flys.append(fly)
            return flys

        return load_actions() + unload_actions() + fly_actions()

    def actions(self, state: str) -> list:
        """ Return the actions that can be executed in the given state.

        :param state: str
            state represented as T/F string of mapped fluents (state variables)
            e.g. 'FTTTFF'
        :return: list of Action objects
        """

        #  init KB Prop with the received state
        kb = PropKB()
        kb.tell(decode_state(state, self.state_map).pos_sentence())

        # search for possible actions
        possible_actions = []
        for action in self.actions_list:

            # Start saying that any action is possible, it will be tested beyond
            is_possible_action = True

            # Check if it is really possible
            for act_pre_condition_neg in action.precond_neg:
                if act_pre_condition_neg in kb.clauses:
                    is_possible_action = False
                    break  # No need to keep searching

            # if current action still probably possible,
            # so check if it is not missed at kb.clauses
            if is_possible_action:
                for act_pre_condition_pos in action.precond_pos:
                    if act_pre_condition_pos not in kb.clauses:
                        is_possible_action = False
                        break  # No need to keep searching

            # if it still a possible action, so it really is, so add it
            if is_possible_action: possible_actions.append(action)

        # return only the possible actions
        return possible_actions

    def result(self, state: str, action: Action):
        """ Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).

        :param state: state entering node
        :param action: Action applied
        :return: resulting state after action
        """

        # init vars
        new_state = FluentState([], [])
        prev_state = decode_state(state, self.state_map)

        # append the FluentState on it appropriate new_state List
        for fluent in prev_state.pos: new_state.pos.append(fluent) if fluent not in action.effect_rem else None
        for fluent in prev_state.neg: new_state.neg.append(fluent) if fluent not in action.effect_add else None
        for fluent in action.effect_add: new_state.pos.append(fluent) if fluent not in new_state.pos else None
        for fluent in action.effect_rem: new_state.neg.append(fluent) if fluent not in new_state.neg else None

        # return it encoded new state
        return encode_state(new_state, self.state_map)

    def goal_test(self, state: str) -> bool:
        """ Test the state to see if goal is reached

        :param state: str representing state
        :return: bool
        """
        kb = PropKB()
        kb.tell(decode_state(state, self.state_map).pos_sentence())
        for clause in self.goal:
            if clause not in kb.clauses:
                return False
        return True

    def h_1(self, node: Node):
        # note that this is not a true heuristic
        h_const = 1
        return h_const

    @lru_cache(maxsize=8192)
    def h_pg_levelsum(self, node: Node):
        """This heuristic uses a planning graph representation of the problem
        state space to estimate the sum of all actions that must be carried
        out from the current state in order to satisfy each individual goal
        condition.
        """
        # requires implemented PlanningGraph class
        pg = PlanningGraph(self, node.state)
        pg_levelsum = pg.h_levelsum()
        return pg_levelsum

    @lru_cache(maxsize=8192)
    def h_ignore_preconditions(self, node: Node):
        """This heuristic estimates the minimum number of actions that must be
        carried out from the current state in order to satisfy all of the goal
        conditions by ignoring the preconditions required for an action to be
        executed.
        """
        # DONE: implement (see Russell-Norvig Ed-3 10.2.3  or Russell-Norvig Ed-2 11.2)

        # Init KB propositional logic to extract it clauses
        count = 0
        kb = PropKB()
        kb.tell(decode_state(node.state, self.state_map).pos_sentence())
        kb_clauses = kb.clauses

        # Count the amount of KB Clauses are in the GOAL,
        # which means the amount of predictions to ignore,
        # because it is already taken
        for clause in self.goal:
            if clause not in kb_clauses:
                count += 1
        return count


def air_cargo_p1() -> AirCargoProblem:
    """
    Init(At(C1, SFO) ∧ At(C2, JFK)
        ∧ At(P1, SFO) ∧ At(P2, JFK)
        ∧ Cargo(C1) ∧ Cargo(C2)
        ∧ Plane(P1) ∧ Plane(P2)
        ∧ Airport(JFK) ∧ Airport(SFO))
    Goal(At(C1, JFK) ∧ At(C2, SFO))

    :return: AirCargoProblem
    """

    cargos = ['C1', 'C2']
    planes = ['P1', 'P2']
    airports = ['JFK', 'SFO']
    pos = [expr('At(C1, SFO)'),
           expr('At(C2, JFK)'),
           expr('At(P1, SFO)'),
           expr('At(P2, JFK)'),
           ]
    neg = [expr('At(C2, SFO)'),
           expr('In(C2, P1)'),
           expr('In(C2, P2)'),
           expr('At(C1, JFK)'),
           expr('In(C1, P1)'),
           expr('In(C1, P2)'),
           expr('At(P1, JFK)'),
           expr('At(P2, SFO)'),
           ]
    init = FluentState(pos, neg)
    goal = [expr('At(C1, JFK)'),
            expr('At(C2, SFO)'),
            ]
    return AirCargoProblem(cargos, planes, airports, init, goal)


def air_cargo_p2() -> AirCargoProblem:
    """
    Init(At(C1, SFO) ∧ At(C2, JFK) ∧ At(C3, ATL)
        ∧ At(P1, SFO) ∧ At(P2, JFK) ∧ At(P3, ATL)
        ∧ Cargo(C1) ∧ Cargo(C2) ∧ Cargo(C3)
        ∧ Plane(P1) ∧ Plane(P2) ∧ Plane(P3)
        ∧ Airport(JFK) ∧ Airport(SFO) ∧ Airport(ATL))
    Goal(At(C1, JFK) ∧ At(C2, SFO) ∧ At(C3, SFO))

    :return: AirCargoProblem
    """

    # Variables to build the syntax
    cargos = ['C1', 'C2', 'C3']
    planes = ['P1', 'P2', 'P3']
    airports = ['JFK', 'SFO', 'ATL']

    # POS Present in the init state expression
    pos = [
        expr('At(C1, SFO)'),
        expr('At(C2, JFK)'),
        expr('At(C3, ATL)'),
        expr('At(P1, SFO)'),
        expr('At(P2, JFK)'),
        expr('At(P3, ATL)')
    ]

    # NEG: States not present in the init state expression
    neg = [
        expr('At(C1, JFK)'), expr('At(C1, ATL)'), expr('In(C1, P1)'), expr('In(C1, P2)'), expr('In(C1, P3)'),
        expr('At(C2, SFO)'), expr('At(C2, ATL)'), expr('In(C2, P1)'), expr('In(C2, P2)'), expr('In(C2, P3)'),
        expr('At(C3, SFO)'), expr('At(C3, JFK)'), expr('In(C3, P1)'), expr('In(C3, P2)'), expr('In(C3, P3)'),
        expr('At(P1, JFK)'), expr('At(P1, ATL)'),
        expr('At(P2, SFO)'), expr('At(P2, ATL)'),
        expr('At(P3, JFK)'), expr('At(P3, SFO)')
    ]

    # Start/init FluentState
    init_state = FluentState(pos, neg)

    # Expected Final State/Result (Goal)
    goal = [
        expr('At(C1, JFK)'),
        expr('At(C2, SFO)'),
        expr('At(C3, SFO)')
    ]

    # DONE: implement Problem 2 definition
    return AirCargoProblem(cargos, planes, airports, init_state, goal)

def air_cargo_p3() -> AirCargoProblem:
    """
    Init(At(C1, SFO) ∧ At(C2, JFK) ∧ At(C3, ATL) ∧ At(C4, ORD)
        ∧ At(P1, SFO) ∧ At(P2, JFK)
        ∧ Cargo(C1) ∧ Cargo(C2) ∧ Cargo(C3) ∧ Cargo(C4)
        ∧ Plane(P1) ∧ Plane(P2)
        ∧ Airport(JFK) ∧ Airport(SFO) ∧ Airport(ATL) ∧ Airport(ORD))
    Goal(At(C1, JFK) ∧ At(C3, JFK) ∧ At(C2, SFO) ∧ At(C4, SFO))

    :return: AirCargoProblem
    """

    # TODO implement Problem 3 definition
    pass
