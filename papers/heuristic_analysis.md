Author: Ilton Garcia dos Santos Silveira
<br>
Date: December, 13, 2017        


# Heuristic Analysis for Planning Cargo

That analysis should expose it project results, showing:
1. The sequence of actions for each problem;
1. Comparing 3 uniformed planning algorithms for all 3 problems;
1. 2 heuristics used with A* search for planning on all 3 problems, from the planning graph;
1. Table of performances for each algorithm on each problem;
1. 1 reason for each result using the appropriate justification.



## The Sequence of Actions for each Problem
Sequence of actions for each problem, comparing 3 uniformed planning algorithms for all 3 problems 
with table of performances.

- Problem 1 initial state and goal:
    ```
    Init(At(C1, SFO) ∧ At(C2, JFK)
    ∧ At(P1, SFO) ∧ At(P2, JFK)
    ∧ Cargo(C1) ∧ Cargo(C2)
    ∧ Plane(P1) ∧ Plane(P2)
    ∧ Airport(JFK) ∧ Airport(SFO))
    Goal(At(C1, JFK) ∧ At(C2, SFO))
    ```
    - RESULT: Problem 1 - astar_search with h_1
    ![Problem 1 - astar_search with h_1](images/results/Problem1-astar_search-h_1.png)
    - RESULT: Problem 1 - depth first graph search
    ![Problem 1 - depth first graph search](images/results/Problem1-depth_first_graph_search.png)
    - RESULT: Problem 1 - uniform cost search
    ![Problem 1 - uniform cost search](images/results/Problem1-uniform_cost_search.png)      
  

- Problem 2 initial state and goal:
    ```
    Init(At(C1, SFO) ∧ At(C2, JFK) ∧ At(C3, ATL) 
        ∧ At(P1, SFO) ∧ At(P2, JFK) ∧ At(P3, ATL) 
        ∧ Cargo(C1) ∧ Cargo(C2) ∧ Cargo(C3)
        ∧ Plane(P1) ∧ Plane(P2) ∧ Plane(P3)
        ∧ Airport(JFK) ∧ Airport(SFO) ∧ Airport(ATL))
    Goal(At(C1, JFK) ∧ At(C2, SFO) ∧ At(C3, SFO))
    ```
    - RESULT: Problem 2 - astar_search with h_1
    ![Problem 2 - astar_search with h_1](images/results/Problem2-astar_search-h_1.png)  
    - RESULT: Problem 2 - uniform cost search
    ![Problem 2 - uniform cost search](images/results/Problem2-uniform_cost_search.png)
    - RESULT: Problem 2 - depth first graph search
    ![Problem 2 - depth first graph search](images/results/Problem2-depth_first_graph_search1.png)
    ![Problem 2 - depth first graph search](images/results/Problem2-depth_first_graph_search2.png)
    ![Problem 2 - depth first graph search](images/results/Problem2-depth_first_graph_search3.png)
    ![Problem 2 - depth first graph search](images/results/Problem2-depth_first_graph_search4.png)
    ![Problem 2 - depth first graph search](images/results/Problem2-depth_first_graph_search5.png)
    ![Problem 2 - depth first graph search](images/results/Problem2-depth_first_graph_search6.png)              


- Problem 3 initial state and goal:
    ```
    Init(At(C1, SFO) ∧ At(C2, JFK) ∧ At(C3, ATL) ∧ At(C4, ORD) 
        ∧ At(P1, SFO) ∧ At(P2, JFK) 
        ∧ Cargo(C1) ∧ Cargo(C2) ∧ Cargo(C3) ∧ Cargo(C4)
        ∧ Plane(P1) ∧ Plane(P2)
        ∧ Airport(JFK) ∧ Airport(SFO) ∧ Airport(ATL) ∧ Airport(ORD))
    Goal(At(C1, JFK) ∧ At(C3, JFK) ∧ At(C2, SFO) ∧ At(C4, SFO))
    ```
  - RESULT: Problem 3 - astar_search with h_1
    ![Problem 3 - astar_search with h_1](images/results/Problem3-astar_search-h_1.png)  
  - RESULT: Problem 3 - uniform cost search
    ![Problem 3 - uniform cost search](images/results/Problem3-uniform_cost_search.png)
  - RESULT: Problem 3 - depth first graph search
    ![Problem 3 - depth first graph search](images/results/Problem3-depth_first_graph_search1.png)
    ![Problem 3 - depth first graph search](images/results/Problem3-depth_first_graph_search2.png)
    ![Problem 3 - depth first graph search](images/results/Problem3-depth_first_graph_search3.png)    
    

## Comparing 3 uniformed planning algorithms

- Problem 1:
    - Best perform: uniform_cost_search & __astar_search__ (tied)
    - Key metrics comparing to the others algorithms: Both found the same solution which had ~3x less actions 
    than the depth first algorithm. All the key metrics was the same for the both tied algorithms except the execution 
    time, astar was a little bit faster than the uniform_cost;
- Problem 2:
    - Best perform: __uniform_cost_search__ & astar_search (tied)
    - Key metrics comparing to the others algorithms: Both (best algorithms) found the same solution which had ~68,77x 
    less actions than the depth first algorithm. All the key metrics was the same for the both tied algorithms except 
    the execution time, uniform_cost_search was a little bit faster than the astar;
- Problem 3:
    - Best perform: __uniform_cost_search__
    - Key metrics comparing to the others algorithms: The uniform cost & the astar found the best solution which had 
    ~32,66x less actions than the depth first algorithm, but at this time the uniform_cost performance (execution time)
    was significantly faster than the astar_search;        
    

## 2 heuristics used with A* Search

## Table of performances for each algorithm

## Reason for each result


1. __MiniMax Algorithm__: performs a complete depth-first exploration of the game tree and its time cost in real games can be impractical;
1. __Alpha-Beta Pruning__: the second one, alpha-beta pruning, ignores a portion of the search tree that makes no difference to the final choice. According to Russell (Artificial Intelligence: A Modern Approach), when this technique is applied to standard minimax tree, it returns the same move as minimax would.



### Heuristic Evaluation Functions

All my three evaluation functions was based on Udacity evaluation functions: _```improved_score```_ & _```open_move_score```_ :

1. __custom_score_2__: weighted linear function, where opponent’s moves are two times more relevant than the agent’s moves. The motivation of this approach is to influence the agent to prioritize moves that minimize the moves from the opponent before maximize its moves.
1. __custom_score_3__: rewards the agent based on the amount of legal moves that still available, as the Udacity open move score function does, and it also gives an additional reward to the agent if it is in the center of the board. The idea is to motivate the agent to dominate the center when it is possible.
1. __custom_score__: it is a mix of the both previous approaches, using weights giving more relevance to opponent's moves, but also giving additional reward when the agent moves to the center of the board. This way it dominates the center paynig attention on opponent's moves.

As a Result I got:

| Opponent    | AB_Improved | AB_Custom | AB_Custom_2 | AB_Custom_3 |
|-------------|-------------|-----------|-------------|-------------|
| Random      |    9 / 1    | 10 / 0    |    10 / 0   |    8 / 2    |
| MM_Open     |    8 / 2    |   8 / 2   |    8 / 2    |    6 / 4    |
| MM_Center   |   10 / 0    |   9 / 1   |    5 / 5    |    7 / 3    |
| MM_Improved |    6 / 4    |   7 / 3   |    7 / 3    |    10 / 0   |
| AB_Open     |    5 / 5    |   4 / 6   |    6 / 4    |    6 / 4    |
| AB_Center   |    7 / 3    |   4 / 6   |    6 / 4    |    6 / 4    |
| AB_Improved |    6 / 4    |   5 / 5   |    8 / 2    |    4 / 6    |
| WIN RATE    |    72.0%    |   67.0%   |    74.0%    |    67.0%    |

So, by this result I choose my AB_Custom_2 as the winner strategy because it won 74.0%, the best WIN RATE.
As the __custom_score__ a mix of strategy 2 & strategy 3 I expected that it would be the better answer. But it proved that using this approach is better only against a Random & MM Agents, against AB Agents it mix become vulnerable. Another conclusion is that the mix between 2 and 3 performed exactly the same as the strategy 3 on WIN RATE perspective, which means that the mix brought no "globally" improvements for AB3 & down the AB2 perform.

According to the video "16 Solving 5x5 Isolation", Malcolm Haines explained how he got better results moving by the edges instead of using the center (my strategy for score_3), and considering the edges he could explore the advantage that the edges looks & work as mirrors each other, reducing the search effort. But the most important is that moving away from the center & paying attention on opponent's moves, reflecting it, the better way is to take a decision based on the situation (opponents reactions), not following a fixed strategy, which can be reflected.   
