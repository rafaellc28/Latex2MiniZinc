enum dmus;

enum outputs;

enum inputs;

array[int, int] of float: outputdata;

array[int, int] of float: inputdata;


array[INDEX_SET_theta_1] of var float: theta;

array[INDEX_SET_lambda_1, INDEX_SET_lambda_2] of var float: lambda;

set of int: INDEX_SET_lambda_1;

set of int: INDEX_SET_lambda_2;

set of int: INDEX_SET_theta_1;


constraint forall(td in dmus)(theta[td] >= 0);

constraint forall(d in dmus, td in dmus)(lambda[d,td] >= 0);

constraint forall(o in outputs, td in dmus)(sum(d in dmus)(lambda[d,td] * outputdata[d,o]) >= outputdata[td,o]);

constraint forall(i in inputs, td in dmus)(sum(d in dmus)(lambda[d,td] * inputdata[d,i]) <= theta[td] * inputdata[td,i]);

constraint forall(td in dmus)(sum(d in dmus)(lambda[d,td]) = 1);



var float: obj = sum(td in dmus)(theta[td]);

solve minimize obj;



