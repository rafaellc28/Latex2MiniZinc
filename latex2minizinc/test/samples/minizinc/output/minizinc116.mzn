set of int: TIME = 1..T;

enum POS = {bank,boat};

set of int: TIME0 = 0..T;

set of int: GUARD = 1..G;

set of int: GUARD0 = 0..G;

set of int: FOOD = 0..F;

set of int: WATER = 0..W;

int: F;

int: W;

int: G;

int: end;

array[int] of POS: opposite = [boat,bank];

int: T;


array[INDEX_SET_pos_1] of var POS: pos;

array[INDEX_SET_food_1] of var FOOD: food;

array[INDEX_SET_water_1] of var WATER: water;

array[INDEX_SET_move_food_1] of var -F..F: move_food;

array[INDEX_SET_move_water_1] of var -W..W: move_water;

set of int: INDEX_SET_food_1 = TIME0;

set of int: INDEX_SET_move_food_1 = TIME;

set of int: INDEX_SET_move_water_1 = TIME;

set of int: INDEX_SET_pos_1 = TIME0;

set of int: INDEX_SET_water_1 = TIME0;


predicate elephant_moves(var FOOD: food_here, var WATER: water_here) =
	let {var FOOD: food_there = F - food_here; var WATER: water_there = W - water_here} in
	food_there = water_there /\ food_there > food_here /\ water_there > water_here;

predicate elephant(var POS: pos, var FOOD: food_here, var WATER: water_here, var POS: new_pos) =
	let {var bool: b = elephant_moves(food_here,water_here)} in
	new_pos = [pos,opposite[pos]][b + 1] /\ (b = true \/ (food_here = 0 <-> water_here = 0));

constraint pos[0] = bank /\ food[0] = F /\ water[0] = W;

constraint forall(t in TIME)(food[t] = food[t - 1] - move_food[t]);

constraint forall(t in TIME)(water[t] = water[t - 1] - move_water[t]);

constraint forall(t in TIME)(abs(move_food[t] + move_water[t]) <= G);

constraint forall(t in TIME)(move_food[t] * move_water[t] >= 0);

constraint forall(t in TIME)(t > end -> (move_food[t] = 0 /\ move_water[t] = 0));

constraint forall(t in TIME)(if pos[t - 1] = bank then elephant(bank,food[t - 1],water[t - 1],pos[t]) else elephant(boat,F - food[t - 1],W - water[t - 1],pos[t]) endif);

constraint pos[end] = boat /\ food[end] = F /\ water[end] = W;

solve satisfy;


