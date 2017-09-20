enum DOGS = {Beagle,Labrador,Shepherd,Boxer};

enum CATS = {Tiger,Lion};

enum FISH = {Goldfish,Guppy,Shark};

set of int: PETS = DOGS_union_CATS_union_FISH;

enum DANGEROUS = {Tiger,Lion,Shark,Crocodile};

set of int: SAFE = PETS_diff_DANGEROUS;

array[INDEX_SET_DOGS_union_CATS_union_FISH] of int: DOGS_union_CATS_union_FISH;

set of int: INDEX_SET_DOGS_union_CATS_union_FISH;

set of int: INDEX_SET_PETS_diff_DANGEROUS;

array[INDEX_SET_PETS_diff_DANGEROUS] of int: PETS_diff_DANGEROUS;




solve satisfy;


