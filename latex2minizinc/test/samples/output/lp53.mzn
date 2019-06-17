enum dmus;

enum outputs;

enum inputs;

array[dmus, outputs] of float: OutputData;

array[dmus, inputs] of float: InputData;


array[dmus] of var float: theta;

array[dmus, dmus] of var float: lambda;


constraint forall(td in dmus)(theta[td] >= 0);

constraint forall(d in dmus, td in dmus)(lambda[d,td] >= 0);

constraint forall(o in outputs, td in dmus)(sum(d in dmus)(lambda[d,td] * OutputData[d,o]) >= OutputData[td,o]);

constraint forall(i in inputs, td in dmus)(sum(d in dmus)(lambda[d,td] * InputData[d,i]) <= theta[td] * InputData[td,i]);

constraint forall(td in dmus)(sum(d in dmus)(lambda[d,td]) = 1);



solve minimize sum(td in dmus)(theta[td]);




