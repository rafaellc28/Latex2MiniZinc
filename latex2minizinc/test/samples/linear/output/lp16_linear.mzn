var float: XB;

var float: XC;


constraint (1 / 200) * XB + (1 / 140) * XC <= 40;

constraint XB <= 6000 /\ XB >= 0;

constraint XC <= 4000 /\ XC >= 0;



solve maximize 25 * XB + 30 * XC;




