array[INDEX_SET_ADJACENT] of set of int: ADJACENT;

array[INDEX_SET_TYPE2, 1..2] of REST: TYPE2;

array[INDEX_SET_ISO, 1..2] of int: ISO;

enum REST;


array[INDEX_SET_Assign2_1, INDEX_SET_Assign2_2, REST] of var int: Assign2;

set of int: INDEX_SET_ADJACENT;

set of int: INDEX_SET_Assign2_1 = ISO;

set of int: INDEX_SET_Assign2_2 = REST;

set of int: INDEX_SET_ISO;

set of int: INDEX_SET_TYPE2;


constraint forall(i1 in INDEX_SET_ISO, j in INDEX_SET_Assign2_2)(Assign2[ISO[i1,1],j,j] >= 0);

constraint forall(i1 in INDEX_SET_ISO, j in REST)(Assign2[ISO[i1,1],ISO[i1,2],j] = 0 \/ Assign2[ISO[i1,1],ISO[i1,2],j] + sum(ii1 in ADJACENT[ISO[i1,1]] where ii1 in INDEX_SET_TYPE2)(Assign2[ii1,ISO[i1,2],j]) >= 2);

solve satisfy;


