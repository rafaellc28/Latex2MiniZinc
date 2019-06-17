array[int] of float: start;

array[int, 1..2] of int: pre;

array[int] of float: duration;


constraint start[pre[i,1]] + duration[pre[i,1]] <= start[pre[i,2]];

solve satisfy;


