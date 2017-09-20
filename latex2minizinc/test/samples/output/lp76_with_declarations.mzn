enum COURSES;

enum STUDENTS;

array[int] of float: credits;

array[int, int] of bool: schedules;

array[INDEX_SET_loads_1] of float: loads = array1d(INDEX_SET_loads_1, [sum(c in COURSES)(schedules[s,c] * credits[c]) | s in STUDENTS]);

set of int: INDEX_SET_loads_1;




solve satisfy;


