enum dmus;

enum outputs;

enum inputs;

array[int, int] of float: OutputData;

array[int, int] of float: InputData;


array[INDEX_SET_theta_1] of var float: theta;

array[INDEX_SET_lambda_1, INDEX_SET_lambda_2] of var float: lambda;

set of int: INDEX_SET_lambda_1 = dmus;

set of int: INDEX_SET_lambda_2 = dmus;

set of int: INDEX_SET_theta_1 = dmus;


constraint forall(td in INDEX_SET_theta_1)(theta[td] >= 0);

constraint forall(d in INDEX_SET_lambda_1, td in INDEX_SET_lambda_2)(lambda[d,td] >= 0);

constraint forall(o in outputs, td in dmus)(sum(d in dmus)(lambda[d,td] * OutputData[d,o]) >= OutputData[td,o]);

constraint forall(i in inputs, td in dmus)(sum(d in dmus)(lambda[d,td] * InputData[d,i]) <= theta[td] * InputData[td,i]);

constraint forall(td in dmus)(sum(d in dmus)(lambda[d,td]) = 1);



solve minimize sum(td in dmus)(theta[td]);




