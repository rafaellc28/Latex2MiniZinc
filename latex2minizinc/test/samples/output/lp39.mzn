enum VALUES;

enum LETTERS;

enum WORDS;

array[int] of float: Total;


array[INDEX_SET_x_1, INDEX_SET_x_2] of var bool: x;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_x_2;


constraint forall(i in LETTERS)(sum(j in VALUES)(x[i,j]) = 1);

constraint forall(j in VALUES)(sum(i in LETTERS)(x[i,j]) = 1);

constraint forall(word in WORDS)(sum(k in 1..length(word), j in VALUES)(j * x[substr(word,to_enum(LETTERS,k),1),j]) = Total[word]);

solve satisfy;


