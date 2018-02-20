enum V;

enum E;

string: file = "graph.eps";

float: R = 2;

int: n;

array[int] of float: x;

array[int] of float: y;

float: x0 = (min(i in V)(x[i])) - R - 3.0;

float: y0 = (min(i in V)(y[i])) - R - 3.0;

float: x1 = (max(i in V)(x[i])) + R + 3.0;

float: y1 = (max(i in V)(y[i])) + R + 3.0;




solve satisfy;


