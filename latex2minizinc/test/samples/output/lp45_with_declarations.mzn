enum COLOR = {blue,green,ivory,red,yellow};

set of int: HOUSE = 1..5;

enum NATIONALITY = {Englishman,Japanese,Norwegian,Spaniard,Ukranian};

enum DRINK = {coffee,milk,orange_juice,tea,water};

enum SMOKE = {Chesterfield,Kools,Lucky_Strike,Old_Gold,Parliament};

enum PET = {dog,fox,horse,snails,zebra};


array[HOUSE, COLOR] of var bool: color;

array[HOUSE, NATIONALITY] of var bool: nationality;

array[HOUSE, DRINK] of var bool: drink;

array[HOUSE, SMOKE] of var bool: smoke;

array[HOUSE, PET] of var bool: pet;


constraint forall(h in HOUSE)(sum(c in COLOR)(color[h,c]) = 1);

constraint forall(c in COLOR)(sum(h in HOUSE)(color[h,c]) = 1);

constraint forall(h in HOUSE)(sum(n in NATIONALITY)(nationality[h,n]) = 1);

constraint forall(n in NATIONALITY)(sum(h in HOUSE)(nationality[h,n]) = 1);

constraint forall(h in HOUSE)(sum(d in DRINK)(drink[h,d]) = 1);

constraint forall(d in DRINK)(sum(h in HOUSE)(drink[h,d]) = 1);

constraint forall(h in HOUSE)(sum(s in SMOKE)(smoke[h,s]) = 1);

constraint forall(s in SMOKE)(sum(h in HOUSE)(smoke[h,s]) = 1);

constraint forall(h in HOUSE)(sum(p in PET)(pet[h,p]) = 1);

constraint forall(p in PET)(sum(h in HOUSE)(pet[h,p]) = 1);

constraint forall(h in HOUSE)(nationality[h,Englishman] = color[h,red]);

constraint forall(h in HOUSE)(nationality[h,Spaniard] = pet[h,dog]);

constraint forall(h in HOUSE)(drink[h,coffee] = color[h,green]);

constraint forall(h in HOUSE)(nationality[h,Ukranian] = drink[h,tea]);

constraint forall(h in HOUSE)(color[h,green] = if h = 1 then 0 else color[h - 1,ivory] endif);

constraint forall(h in HOUSE)(smoke[h,Old_Gold] = pet[h,snails]);

constraint forall(h in HOUSE)(smoke[h,Kools] = color[h,yellow]);

constraint drink[3,milk] = 1;

constraint nationality[1,Norwegian] = 1;

constraint forall(h in HOUSE)((1 - smoke[h,Chesterfield]) + (if h = 1 then 0 else pet[h - 1,fox] endif) + (if h = 5 then 0 else pet[h + 1,fox] endif) >= 1);

constraint forall(h in HOUSE)((1 - smoke[h,Kools]) + (if h = 1 then 0 else pet[h - 1,horse] endif) + (if h = 5 then 0 else pet[h + 1,horse] endif) >= 1);

constraint forall(h in HOUSE)(smoke[h,Lucky_Strike] = drink[h,orange_juice]);

constraint forall(h in HOUSE)(nationality[h,Japanese] = smoke[h,Parliament]);

constraint forall(h in HOUSE)((1 - nationality[h,Norwegian]) + (if h = 1 then 0 else color[h - 1,blue] endif) + (if h = 5 then 0 else color[h + 1,blue] endif) >= 1);

solve satisfy;


