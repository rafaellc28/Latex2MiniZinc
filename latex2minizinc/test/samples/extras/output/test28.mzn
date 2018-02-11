array[INDEX_SET_ISO, 1..2] of int: ISO;

enum REST;

array[INDEX_SET_ADJACENT] of set of int: ADJACENT;

array[INDEX_SET_TYPE2, 1..2] of REST: TYPE2;

enum PEOPLE;

array[INDEX_SET_upperbnd_1, INDEX_SET_upperbnd_2, INDEX_SET_upperbnd_3] of float: upperbnd = array3d(INDEX_SET_upperbnd_1, INDEX_SET_upperbnd_2, INDEX_SET_upperbnd_3, [min(ceil((number2[ISO[i1,1],ISO[i1,2]]/card(PEOPLE)) * hiDine[j]) + give[ISO[i1,1],ISO[i1,2]],hiTargetTitle[ISO[i1,1],j] + giveTitle[ISO[i1,1]],hiTargetLoc[ISO[i1,2],j] + giveLoc[ISO[i1,2]],number2[ISO[i1,1],ISO[i1,2]]) | i1 in INDEX_SET_ISO, j in REST]);

array[int, int] of float: number2;

array[int] of float: hiDine;

array[int, int] of float: give;

array[int] of float: giveTitle;

array[int, int] of float: hiTargetLoc;

array[int] of float: giveLoc;


array[INDEX_SET_Lone_1, INDEX_SET_Lone_2, INDEX_SET_Lone_3] of var bool: Lone;

array[INDEX_SET_Assign2_1, INDEX_SET_Assign2_2, INDEX_SET_Assign2_3] of var int: Assign2;

array[INDEX_SET_hiTargetTitle_1, INDEX_SET_hiTargetTitle_2] of var int: hiTargetTitle;

set of int: INDEX_SET_ADJACENT;

set of int: INDEX_SET_Assign2_1;

set of int: INDEX_SET_Assign2_2;

set of int: INDEX_SET_Assign2_3;

set of int: INDEX_SET_ISO;

set of int: INDEX_SET_Lone_1;

set of int: INDEX_SET_Lone_2;

set of int: INDEX_SET_Lone_3;

set of int: INDEX_SET_TYPE2;

set of int: INDEX_SET_hiTargetTitle_1;

set of int: INDEX_SET_hiTargetTitle_2;

set of int: INDEX_SET_upperbnd_1;

set of int: INDEX_SET_upperbnd_2;

set of int: INDEX_SET_upperbnd_3;


constraint forall(i1 in INDEX_SET_ISO, j in REST)(Assign2[ISO[i1,1],j,j] >= 0);

constraint forall(i0 in INDEX_SET_hiTargetTitle_1, i1 in INDEX_SET_hiTargetTitle_2)(hiTargetTitle[i0,i1] >= 0);

constraint forall(i1 in INDEX_SET_ISO, j in REST)(Assign2[ISO[i1,1],ISO[i1,2],j] <= upperbnd[ISO[i1,1],ISO[i1,2],j] * Lone[ISO[i1,1],ISO[i1,2],j]);

constraint forall(i1 in INDEX_SET_ISO, j in REST)(Assign2[ISO[i1,1],ISO[i1,2],j] + sum(ii1 in ADJACENT[ISO[i1,1]] where ii1 in INDEX_SET_TYPE2)(Assign2[ii1,ISO[i1,2],j]) >= 2 * Lone[ISO[i1,1],ISO[i1,2],j]);

constraint forall(i1 in INDEX_SET_ISO, j in REST)(Assign2[ISO[i1,1],ISO[i1,2],j] >= Lone[ISO[i1,1],ISO[i1,2],j]);

solve satisfy;


