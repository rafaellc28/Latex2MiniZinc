set of int: SQUARE = 1..n;

set of int: NSQ = 1..nsq;

array[SQUARE] of int: ncopy;

int: nsq = sum(i in SQUARE)(ncopy[i]);

int: n;

int: maxl = sum(i in SQUARE)(i * ncopy[i]);

int: mina = sum(i in SQUARE)(i * i * ncopy[i]);


var n..maxl: height;

var n..maxl: width;

var mina..floor(n * maxl): area = height * width;

array[NSQ] of var 0..maxl: x;

array[NSQ] of var 0..maxl: y;

array[NSQ] of var SQUARE: size;


include "global_cardinality.mzn";

constraint global_cardinality(size,[i | i in SQUARE],ncopy);

constraint forall(i in 1..floor(nsq - 1))(size[i] <= size[i + 1]);

constraint forall(s in NSQ)(x[s] + size[s] <= width);

constraint forall(s in NSQ)(y[s] + size[s] <= height);

constraint forall(s1,s2 in NSQ where s1 < s2)(x[s1] + size[s1] <= x[s2] \/ x[s2] + size[s2] <= x[s1] \/ y[s1] + size[s1] <= y[s2] \/ y[s2] + size[s2] <= y[s1]);



solve minimize area;




