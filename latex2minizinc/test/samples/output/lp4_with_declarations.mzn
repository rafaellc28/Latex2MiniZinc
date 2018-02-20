var float: bin1;

var float: bin2;

var float: bin3;

var float: bin4;

var float: bin5;

var float: alum;

var float: silicon;


constraint bin1 >= 0 /\ bin1 <= 200;

constraint bin2 >= 0 /\ bin2 <= 2500;

constraint bin3 >= 400 /\ bin3 <= 800;

constraint bin4 >= 100 /\ bin4 <= 700;

constraint bin5 >= 0 /\ bin5 <= 1500;

constraint alum >= 0;

constraint silicon >= 0;

constraint bin1 + bin2 + bin3 + bin4 + bin5 + alum + silicon = 2000;

constraint 0.15 * bin1 + 0.04 * bin2 + 0.02 * bin3 + 0.04 * bin4 + 0.02 * bin5 + 0.01 * alum + 0.03 * silicon <= 60;

constraint 0.03 * bin1 + 0.05 * bin2 + 0.08 * bin3 + 0.02 * bin4 + 0.06 * bin5 + 0.01 * alum <= 100;

constraint 0.02 * bin1 + 0.04 * bin2 + 0.01 * bin3 + 0.02 * bin4 + 0.02 * bin5 <= 40;

constraint 0.02 * bin1 + 0.03 * bin2 + 0.01 * bin5 <= 30;

constraint 0.70 * bin1 + 0.75 * bin2 + 0.80 * bin3 + 0.75 * bin4 + 0.80 * bin5 + 0.97 * alum >= 1500;

constraint 0.02 * bin1 + 0.06 * bin2 + 0.08 * bin3 + 0.12 * bin4 + 0.02 * bin5 + 0.01 * alum + 0.97 * silicon <= 300 /\ 0.02 * bin1 + 0.06 * bin2 + 0.08 * bin3 + 0.12 * bin4 + 0.02 * bin5 + 0.01 * alum + 0.97 * silicon >= 250;



solve minimize 0.03 * bin1 + 0.08 * bin2 + 0.17 * bin3 + 0.12 * bin4 + 0.15 * bin5 + 0.21 * alum + 0.38 * silicon;




