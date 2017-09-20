enum Sample;

array[int] of float: Sx;

array[int] of float: Sy;


var float: X;

array[INDEX_SET_Ex_1] of var float: Ex;

var float: Y;

array[INDEX_SET_Ey_1] of var float: Ey;

set of int: INDEX_SET_Ex_1;

set of int: INDEX_SET_Ey_1;


constraint forall(z in Sample)(X + Ex[z] = Sx[z]);

constraint sum(z in Sample)(Ex[z]) = 0;

constraint forall(z in Sample)(Y + Ey[z] = Sy[z]);

constraint sum(z in Sample)(Ey[z]) = 0;

solve satisfy;


