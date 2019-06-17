enum COURSES;

enum STUDENTS;

array[COURSES] of float: credits;

array[STUDENTS, COURSES] of bool: schedules;

array[STUDENTS] of float: loads = array1d(STUDENTS, [sum(c in COURSES)(schedules[s,c] * credits[c]) | s in STUDENTS]);


constraint forall(c in COURSES)(assert(credits[c] >= 0, "Assertion credits[\(c)] >= 0 failed!"));



solve satisfy;


