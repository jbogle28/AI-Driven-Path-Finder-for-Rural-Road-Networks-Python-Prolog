:- dynamic road/5.
:- dynamic location/1.

% Locations
location('Christiana').
location('Frankfield').
location('Knockpatrick').
location('Lionel_Town').
location('Mandeville').
location('May_Pen').
location('Mile_Gully').
location('Newport').
location('Porus').
location('Spaldings').

% Roads: road(Source, Destination, Distance, Type, Status)
road('Mandeville', 'Christiana', 12.0, paved, open).
road('Christiana', 'Mandeville', 12.0, paved, open).
road('Mandeville', 'Mile_Gully', 8.0, unpaved, open).
road('Mile_Gully', 'Mandeville', 8.0, unpaved, open).
road('Christiana', 'Spaldings', 15.0, paved, open).
road('Spaldings', 'Christiana', 15.0, paved, open).
road('Mile_Gully', 'Porus', 10.0, broken_cistern, open).
road('Porus', 'Mile_Gully', 10.0, broken_cistern, open).
road('Porus', 'May_Pen', 18.0, paved, closed).
road('May_Pen', 'Porus', 18.0, paved, closed).
road('Spaldings', 'May_Pen', 20.0, deep_pothole, open).
road('May_Pen', 'Spaldings', 20.0, deep_pothole, open).
road('May_Pen', 'Lionel_Town', 14.0, paved, open).
road('Lionel_Town', 'May_Pen', 14.0, paved, open).
road('May_Pen', 'Frankfield', 10.0, paved, open).
road('Frankfield', 'May_Pen', 10.0, paved, open).
road('Frankfield', 'Mandeville', 22.0, unpaved, open).
road('Mandeville', 'Frankfield', 22.0, unpaved, open).
road('Newport', 'Christiana', 7.0, paved, open).
road('Christiana', 'Newport', 7.0, paved, open).
road('Newport', 'Knockpatrick', 5.0, unpaved, open).
road('Knockpatrick', 'Newport', 5.0, unpaved, open).
road('Knockpatrick', 'Spaldings', 9.0, deep_pothole, open).
road('Spaldings', 'Knockpatrick', 9.0, deep_pothole, open).

connected(X, Y) :- road(X, Y, _, _, _).

road_weight(Source, Dest, Distance, distance) :-
    road(Source, Dest, Distance, _, open).

road_weight(Source, Dest, Distance, avoid_unpaved) :-
    road(Source, Dest, Distance, Type, open),
    Type \= unpaved.

road_weight(Source, Dest, Distance, avoid_closed) :-
    road(Source, Dest, Distance, _, open).

road_weight(Source, Dest, Distance, avoid_broken_cistern) :-
    road(Source, Dest, Distance, Type, open),
    Type \= broken_cistern.

road_weight(Source, Dest, Distance, avoid_deep_pothole) :-
    road(Source, Dest, Distance, Type, open),
    Type \= deep_pothole.

% Dijkstra
dijkstra_path(Start, Goal, Path, TotalDistance, Criteria) :-
    dijkstra([[0, Start, []]], Goal, Path, TotalDistance, Criteria).

dijkstra([[Cost, Goal, PathSoFar]|_], Goal, Path, Cost, _) :-
    reverse([Goal|PathSoFar], Path).

dijkstra([[Cost, Current, PathSoFar]|Rest], Goal, Path, TotalCost, Criteria) :-
    findall([NewCost, Next, [Current|PathSoFar]],
            (road_weight(Current, Next, Weight, Criteria),
             \+ member(Next, PathSoFar),
             NewCost is Cost + Weight),
            NewPaths),
    append(Rest, NewPaths, AllPaths),
    sort(AllPaths, SortedPaths),
    dijkstra(SortedPaths, Goal, Path, TotalCost, Criteria).
% BFS 
bfs_path(Start, Goal, Path) :-
    bfs_search([[Start]], Goal, RevPath),
    reverse(RevPath, Path).

bfs_search([[Goal|Rest]|_], Goal, [Goal|Rest]) :- !.

bfs_search([CurrentPath|RestPaths], Goal, FinalPath) :-
    CurrentPath = [Node|_],
    findall([Next|CurrentPath],
            (road(Node, Next, _, _, open),
             \+ member(Next, CurrentPath)),
            Extensions),
    append(RestPaths, Extensions, NewPaths),
    bfs_search(NewPaths, Goal, FinalPath).

% Helper functions
get_children(Node, ChildList) :-
    findall(Child, road(Node, Child, _, _, open), ChildList).

% Database operations
add_location(Name) :-
    (location(Name) -> true ; assertz(location(Name))).

add_road(Source, Dest, Distance, Type, Status) :-
    add_location(Source),
    add_location(Dest),
    retractall(road(Source, Dest, _, _, _)),
    retractall(road(Dest, Source, _, _, _)),
    assertz(road(Source, Dest, Distance, Type, Status)),
    assertz(road(Dest, Source, Distance, Type, Status)).

update_road(Source, Dest, Distance, Type, Status) :-
    retractall(road(Source, Dest, _, _, _)),
    retractall(road(Dest, Source, _, _, _)),
    assertz(road(Source, Dest, Distance, Type, Status)),
    assertz(road(Dest, Source, Distance, Type, Status)).

update_road_status(Source, Dest, NewStatus) :-
    road(Source, Dest, Distance, Type, _),
    retractall(road(Source, Dest, _, _, _)),
    retractall(road(Dest, Source, _, _, _)),
    assertz(road(Source, Dest, Distance, Type, NewStatus)),
    assertz(road(Dest, Source, Distance, Type, NewStatus)).

update_road_type(Source, Dest, NewType) :-
    road(Source, Dest, Distance, _, Status),
    retractall(road(Source, Dest, _, _, _)),
    retractall(road(Dest, Source, _, _, _)),
    assertz(road(Source, Dest, Distance, NewType, Status)),
    assertz(road(Dest, Source, Distance, NewType, Status)).

delete_road(Source, Dest) :-
    retractall(road(Source, Dest, _, _, _)),
    retractall(road(Dest, Source, _, _, _)).

get_road(Source, Dest, Distance, Type, Status) :-
    road(Source, Dest, Distance, Type, Status).

get_all_locations(Locations) :-
    findall(Loc, location(Loc), Locations).

get_all_roads(Roads) :-
    findall(road(S, D, Dist, Type, Status), road(S, D, Dist, Type, Status), Roads).
/*
% Dijkstra trace 
dijkstra_path_trace(Start, Goal, Path, TotalDistance, Criteria) :-
    write('Starting Dijkstra from '), write(Start), write(' to '), write(Goal), 
    write(' (Criteria: '), write(Criteria), write(')'), nl,
    dijkstra_trace([[0, Start, []]], Goal, Path, TotalDistance, Criteria),
    write('Path found: '), write(Path), write(' (Total Distance: '), write(TotalDistance), write(' km)'), nl.

dijkstra_trace([[Cost, Goal, PathSoFar]|_], Goal, Path, Cost, _) :-
    write('  Reached goal: '), write(Goal), write(' with cost '), write(Cost), nl,
    reverse([Goal|PathSoFar], Path).

dijkstra_trace([[Cost, Current, PathSoFar]|Rest], Goal, Path, TotalCost, Criteria) :-
    write('  Exploring: '), write(Current), write(' (Current cost: '), write(Cost), write(')'), nl,
    findall([NewCost, Next, [Current|PathSoFar]],
            (road_weight(Current, Next, Weight, Criteria),
             \+ member(Next, PathSoFar),
             NewCost is Cost + Weight,
             write('    -> '), write(Next), write(' (cost: '), write(NewCost), write(')'), nl),
            NewPaths),
    append(Rest, NewPaths, AllPaths),
    sort(AllPaths, SortedPaths),
    dijkstra_trace(SortedPaths, Goal, Path, TotalCost, Criteria).

% BFS with trace 
bfs_path_trace(Start, Goal, Path) :-
    write('Starting BFS from '), write(Start), write(' to '), write(Goal), nl,
    bfs_search_trace([[Start]], Goal, RevPath),
    reverse(RevPath, Path),
    write('Path found: '), write(Path), nl.

bfs_search_trace([[Goal|Rest]|_], Goal, [Goal|Rest]) :- 
    write('  Reached goal: '), write(Goal), nl, !.

bfs_search_trace([CurrentPath|RestPaths], Goal, FinalPath) :-
    CurrentPath = [Node|_],
    write('  Current node: '), write(Node), write(' (Path: '), write(CurrentPath), write(')'), nl,
    findall([Next|CurrentPath],
            (road(Node, Next, _, _, open),
             \+ member(Next, CurrentPath),
             write('    Found neighbor: '), write(Next), nl),
            Extensions),
    append(RestPaths, Extensions, NewPaths),
    bfs_search_trace(NewPaths, Goal, FinalPath).
    */