enum Sample;

array[Sample] of float: Sx;

array[Sample] of float: Sy;


var float: X;

var float: Y;

array[Sample] of var float: Ex;

array[Sample] of var float: Ey;


constraint forall(z in Sample)(X + Ex[z] = Sx[z]);

constraint sum(z in Sample)(Ex[z]) = 0;

constraint forall(z in Sample)(Y + Ey[z] = Sy[z]);

constraint sum(z in Sample)(Ey[z]) = 0;

solve satisfy;


