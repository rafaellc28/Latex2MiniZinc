int: year = 2010;

array[int] of int: firstday;

array[int] of int: daysinmonth;

array[INDEX_SET_foo_1, INDEX_SET_foo_2, INDEX_SET_foo_3] of int: foo = array3d(INDEX_SET_foo_1, INDEX_SET_foo_2, INDEX_SET_foo_3, [7 * k + d + 1 - firstday[m] | m in 1..12, k in 0..5, d in 0..6]);

array[INDEX_SET_cal_1, INDEX_SET_cal_2, INDEX_SET_cal_3] of int: cal = array3d(INDEX_SET_cal_1, INDEX_SET_cal_2, INDEX_SET_cal_3, [if 1 <= foo[m,k,d] /\ foo[m,k,d] <= daysinmonth[m] then foo[m,k,d] else 0 endif | m in 1..12, k in 0..5, d in 0..6]);

set of int: INDEX_SET_cal_1;

set of int: INDEX_SET_cal_2;

set of int: INDEX_SET_cal_3;

set of int: INDEX_SET_foo_1;

set of int: INDEX_SET_foo_2;

set of int: INDEX_SET_foo_3;




solve satisfy;


