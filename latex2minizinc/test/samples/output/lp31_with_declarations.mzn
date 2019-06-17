set of int: PRODUCTS;

enum REACTIONS;

set of int: SPECIES;

set of int: RAWMATERIALS;

enum ATOMS;

set of int: BYPRODUCTS = (SPECIES diff RAWMATERIALS diff PRODUCTS);

array[PRODUCTS] of float: mw = array1d(PRODUCTS, [sum(a in ATOMS)(amu[a] * formula[s,a]) | s in PRODUCTS]);

array[SPECIES, REACTIONS] of float: stoich;

array[SPECIES] of float: name;

array[ATOMS] of float: amu;

array[SPECIES, ATOMS] of float: formula;


array[SPECIES] of var float: n;

array[REACTIONS] of var float: x;

set of int: INDEX_SET_SPECIES_diff_RAWMATERIALS;

array[INDEX_SET_SPECIES_diff_RAWMATERIALS] of int: SPECIES_diff_RAWMATERIALS;


constraint forall(a in ATOMS)(assert(amu[a] >= 0, "Assertion amu[\(a)] >= 0 failed!"));

constraint forall(s in SPECIES, a in ATOMS)(assert(formula[s,a] >= 0, "Assertion formula[\(s),\(a)] >= 0 failed!"));

constraint forall(s in SPECIES)(n[s] = sum(r in REACTIONS)(stoich[s,r] * x[r]));

constraint forall(s in RAWMATERIALS)(sum(r in REACTIONS)(n[s]) <= 0);

constraint forall(s in SPECIES_diff_RAWMATERIALS)(sum(r in REACTIONS)(n[s]) >= 0);

constraint sum(s in RAWMATERIALS)(-n[s]) <= 1;



solve maximize sum(s in PRODUCTS)(mw[s] * n[s]);




