enum COURSES;

enum STUDENTS;

array[int] of float: credits;

array[int, int] of bool: schedules;

array[INDEX_SET_loads_1] of float: loads = array1d(INDEX_SET_loads_1, [sum(c in COURSES)(schedules[s,c] * credits[c]) | s in STUDENTS]);

set of int: INDEX_SET_loads_1;


constraint forall(c in COURSES)(assert(credits[c] >= 0, "Assertion credits[\(c)] >= 0 failed!"));



solve satisfy;


