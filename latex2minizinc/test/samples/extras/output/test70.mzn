enum I;

int: a;

int: b;


constraint a in I <-> not(b in I);

solve satisfy;


