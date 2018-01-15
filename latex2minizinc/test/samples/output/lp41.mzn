enum DIGITS;

enum LETTERS;


array[INDEX_SET_x_1, INDEX_SET_x_2] of var bool: x;

array[INDEX_SET_dig_1] of var float: dig;

array[INDEX_SET_carry_1] of var bool: carry;

LETTERS: D;

LETTERS: E;

set of int: INDEX_SET_carry_1 = 1..3;

set of int: INDEX_SET_dig_1;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_x_2;

LETTERS: M;

LETTERS: N;

LETTERS: O;

LETTERS: R;

LETTERS: S;

LETTERS: Y;


constraint forall(i in LETTERS)(sum(d in DIGITS)(x[i,d]) = 1);

constraint forall(d in DIGITS)(sum(i in LETTERS)(x[i,d]) <= 1);

constraint forall(i in LETTERS)(dig[i] = sum(d in DIGITS)(d * x[i,d]));

constraint dig[D] + dig[E] = dig[Y] + 10 * carry[1];

constraint dig[N] + dig[R] + carry[1] = dig[E] + 10 * carry[2];

constraint dig[E] + dig[O] + carry[2] = dig[N] + 10 * carry[3];

constraint dig[S] + dig[M] + carry[3] = dig[O] + 10 * dig[M];

constraint dig[M] >= 1;

constraint forall(i in 1..3)(carry[i] >= 0);

solve satisfy;


