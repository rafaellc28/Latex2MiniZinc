enum dmus;

enum outputs;

enum inputs;

array[dmus, outputs] of float: outputdata;

array[dmus, inputs] of float: inputdata;


array[dmus] of var float: theta;

array[dmus, dmus] of var float: lambda;


constraint forall(td in dmus, o in outputs)(assert(outputdata[td,o] >= 0, "Assertion outputdata[\(td),\(o)] >= 0 failed!"));

constraint forall(td in dmus, i in inputs)(assert(inputdata[td,i] >= 0, "Assertion inputdata[\(td),\(i)] >= 0 failed!"));

constraint forall(td in dmus)(theta[td] >= 0);

constraint forall(d in dmus, td in dmus)(lambda[d,td] >= 0);

constraint forall(o in outputs, td in dmus)(sum(d in dmus)(lambda[d,td] * outputdata[d,o]) >= outputdata[td,o]);

constraint forall(i in inputs, td in dmus)(sum(d in dmus)(lambda[d,td] * inputdata[d,i]) <= theta[td] * inputdata[td,i]);

constraint forall(td in dmus)(sum(d in dmus)(lambda[d,td]) = 1);



solve minimize sum(td in dmus)(theta[td]);




