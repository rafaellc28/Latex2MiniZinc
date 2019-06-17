int: year = 2010;

array[1..12] of int: firstday = array1d(1..12, [time2str(str2time(year ++ "-" ++ m ++ "-01","%Y-%m-%d"),"%w") | m in 1..12]);

array[1..12] of int: daysinmonth = array1d(1..12, [(str2time(year + (if m < 12 then 0 else 1 endif) ++ "-" ++ (if m < 12 then m + 1 else 1 endif) ++ "-01","%Y-%m-%d") - str2time(year ++ "-" ++ m ++ "-01","%Y-%m-%d")) / 86400 | m in 1..12]);

array[1..12, 0..5, 0..6] of int: foo = array3d(1..12, 0..5, 0..6, [7 * k + d + 1 - firstday[m] | m in 1..12, k in 0..5, d in 0..6]);

array[1..12, 0..5, 0..6] of int: cal = array3d(1..12, 0..5, 0..6, [if 1 <= foo[m,k,d] /\ foo[m,k,d] <= daysinmonth[m] then foo[m,k,d] else 0 endif | m in 1..12, k in 0..5, d in 0..6]);




solve satisfy;


