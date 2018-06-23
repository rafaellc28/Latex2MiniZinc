enum PRODUCTS;

enum REACTIONS;

set of int: SPECIES;

set of int: RAWMATERIALS;

array[int] of float: MW;

array[int, int] of float: Stoich;


array[INDEX_SET_n_1] of var float: n;

array[INDEX_SET_x_1] of var float: x;

set of int: INDEX_SET_SPECIES_diff_RAWMATERIALS;

set of int: INDEX_SET_n_1 = SPECIES;

set of int: INDEX_SET_x_1 = REACTIONS;

array[INDEX_SET_SPECIES_diff_RAWMATERIALS] of int: SPECIES_diff_RAWMATERIALS;


constraint forall(s in SPECIES)(n[s] = sum(r in REACTIONS)(Stoich[s,r] * x[r]));

constraint forall(s in RAWMATERIALS)(sum(r in REACTIONS)(n[s]) <= 0);

constraint forall(s in SPECIES_diff_RAWMATERIALS)(sum(r in REACTIONS)(n[s]) >= 0);

constraint sum(s in RAWMATERIALS)(-n[s]) <= 1;

constraint forall(s in SPECIES)(n[s] <= 1);



solve maximize sum(s in PRODUCTS)(MW[s] * n[s]);




