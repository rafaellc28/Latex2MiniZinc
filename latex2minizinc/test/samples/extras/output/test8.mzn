set of int: J = 1..n;

set of int: M = 1..m;

int: m;

int: n;


constraint assert(m > 0, "Assertion m > 0 failed!");

constraint assert(n > 0, "Assertion n > 0 failed!");



solve satisfy;


