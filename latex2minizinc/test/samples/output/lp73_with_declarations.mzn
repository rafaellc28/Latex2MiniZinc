int: year = 2010;

array[INDEX_SET_firstday_1] of int: firstday = array1d(INDEX_SET_firstday_1, [time2str(str2time(year ++ "-" ++ m ++ "-01","%Y-%m-%d"),"%w") | m in 1..12]);

array[INDEX_SET_daysinmonth_1] of int: daysinmonth = array1d(INDEX_SET_daysinmonth_1, [(str2time(year + (if m < 12 then 0 else 1 endif) ++ "-" ++ (if m < 12 then m + 1 else 1 endif) ++ "-01","%Y-%m-%d") - str2time(year ++ "-" ++ m ++ "-01","%Y-%m-%d")) / 86400 | m in 1..12]);

array[INDEX_SET_foo_1, INDEX_SET_foo_2, INDEX_SET_foo_3] of int: foo = array3d(INDEX_SET_foo_1, INDEX_SET_foo_2, INDEX_SET_foo_3, [7 * k + d + 1 - firstday[m] | m in 1..12, k in 0..5, d in 0..6]);

array[INDEX_SET_cal_1, INDEX_SET_cal_2, INDEX_SET_cal_3] of int: cal = array3d(INDEX_SET_cal_1, INDEX_SET_cal_2, INDEX_SET_cal_3, [if 1 <= foo[m,k,d] /\ foo[m,k,d] <= daysinmonth[m] then foo[m,k,d] else 0 endif | m in 1..12, k in 0..5, d in 0..6]);

set of int: INDEX_SET_cal_1 = 1..12;

set of int: INDEX_SET_cal_2 = 0..5;

set of int: INDEX_SET_cal_3 = 0..6;

set of int: INDEX_SET_daysinmonth_1 = 1..12;

set of int: INDEX_SET_firstday_1 = 1..12;

set of int: INDEX_SET_foo_1 = 1..12;

set of int: INDEX_SET_foo_2 = 0..5;

set of int: INDEX_SET_foo_3 = 0..6;




solve satisfy;


