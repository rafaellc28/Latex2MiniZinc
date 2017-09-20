enum PRODUCTS;

enum REACTIONS;

enum SPECIES;

enum RAWMATERIALS;

enum ATOMS;

set of int: BYPRODUCTS = SPECIES_diff_RAWMATERIALS_diff_PRODUCTS;

array[INDEX_SET_mw_1] of float: mw = array1d(INDEX_SET_mw_1, [sum(a in ATOMS)(amu[a] * formula[s,a]) | s in PRODUCTS]);

array[int, int] of float: stoich;

array[int] of float: name;

array[int] of float: amu;

array[int, int] of float: formula;


array[INDEX_SET_n_1] of var float: n;

array[INDEX_SET_x_1] of var float: x;

set of int: INDEX_SET_SPECIES_diff_RAWMATERIALS;

set of int: INDEX_SET_SPECIES_diff_RAWMATERIALS_diff_PRODUCTS;

set of int: INDEX_SET_mw_1;

set of int: INDEX_SET_n_1;

set of int: INDEX_SET_x_1;

array[INDEX_SET_SPECIES_diff_RAWMATERIALS] of int: SPECIES_diff_RAWMATERIALS;

array[INDEX_SET_SPECIES_diff_RAWMATERIALS_diff_PRODUCTS] of int: SPECIES_diff_RAWMATERIALS_diff_PRODUCTS;


constraint forall(s in SPECIES)(n[s] = sum(r in REACTIONS)(stoich[s,r] * x[r]));

constraint forall(s in RAWMATERIALS)(sum(r in REACTIONS)(n[s]) <= 0);

constraint forall(s in SPECIES_diff_RAWMATERIALS)(sum(r in REACTIONS)(n[s]) >= 0);

constraint sum(s in RAWMATERIALS)(-n[s]) <= 1;



var float: obj = sum(s in PRODUCTS)(mw[s] * n[s]);

solve maximize obj;




