var float: R;

var float: P;

var float: B1;

var float: B2;

var float: B3;

var float: B4;

var 0.0..2.0: I;


constraint B1 = P * (1.0 + I) - R;

constraint B2 = B1 * (1.0 + I) - R;

constraint B3 = B2 * (1.0 + I) - R;

constraint B4 = B3 * (1.0 + I) - R;

solve satisfy;


