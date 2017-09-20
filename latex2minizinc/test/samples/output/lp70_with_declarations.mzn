enum Sample;

array[int] of float: Sx;

array[int] of float: Sy;


var float: a;

var float: b;


constraint sum(z in Sample)(a * Sx[z] * Sx[z] + sum(z in Sample)(b * Sx[z])) = sum(z in Sample)(Sy[z] * Sx[z]);

constraint sum(z in Sample)(a * Sx[z] + sum(z in Sample)(b)) = sum(z in Sample)(Sy[z]);

solve satisfy;


