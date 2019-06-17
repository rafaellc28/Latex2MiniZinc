set of int: SQUARE = 1..n;

set of int: NSQ = 1..nsq;

array[SQUARE] of int: ncopy;

int: nsq = sum(i in SQUARE)(ncopy[i]);

array[SQUARE] of int: base = [if i = 1 then 0 else sum(j in 1..floor(i - 1))(ncopy[j]) endif | i in SQUARE];

int: n;

int: maxl = sum(i in SQUARE)(i * ncopy[i]);

int: mina = sum(i in SQUARE)(i * i * ncopy[i]);


var n..maxl: height;

var n..maxl: width;

var mina..floor(n * maxl): area = height * width;

array[NSQ] of var 0..maxl: x;

array[NSQ] of var 0..maxl: y;

array[NSQ] of var SQUARE: size = [max(j in SQUARE)(j * (i > base[j])) | i in NSQ];


include "global_cardinality.mzn";

include "cumulative.mzn";

include "diffn.mzn";

include "lex_greater.mzn";

constraint global_cardinality(size,[i | i in SQUARE],ncopy);

constraint forall(i in 1..floor(nsq - 1))(size[i] <= size[i + 1]);

constraint forall(s in NSQ)(x[s] + size[s] <= width);

constraint forall(s in NSQ)(y[s] + size[s] <= height);

constraint diffn(x,y,size,size);

constraint cumulative(x,size,size,height);

constraint cumulative(y,size,size,width);

constraint forall(i in SQUARE)(forall(j in 1..floor(ncopy[i] - 1))(lex_greater([x[base[i] + j],y[base[i] + j]],[x[base[i] + j + 1],y[base[i] + j + 1]])));



solve minimize area;




