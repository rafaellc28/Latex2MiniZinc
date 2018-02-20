array[INDEX_SET_B, 1..6] of int: B;

enum rows;

enum cols;


array[INDEX_SET_x_1, INDEX_SET_x_2, INDEX_SET_x_3, INDEX_SET_x_4, INDEX_SET_x_5, INDEX_SET_x_6] of var bool: x;

set of int: INDEX_SET_B;

set of int: INDEX_SET_rows_cols;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_x_2;

set of int: INDEX_SET_x_3;

set of int: INDEX_SET_x_4;

set of int: INDEX_SET_x_5;

set of int: INDEX_SET_x_6;

array[INDEX_SET_rows_cols,1..2] of int: rows_cols;


constraint forall(s in INDEX_SET_rows_cols)(sum(i in INDEX_SET_B where rows_cols[s,1] >= B[i,3] /\ rows_cols[s,1] < B[i,5] /\ rows_cols[s,2] >= B[i,4] /\ rows_cols[s,2] < B[i,6])(x[B[i,1],B[i,2],B[i,3],B[i,4],B[i,5],B[i,6]]) = 1);



solve minimize 0;




