enum Hatreds;

set of int: Seats = 1..12;

set of int: Guests = 1..12;

array[int] of int: h1 = [groom,carol,ed,bride,ted];

array[int] of int: h2 = [clara,bestman,ted,alice,ron];

int: groom = 2;

int: carol = 6;

int: ed = 11;

int: bride = 1;

int: ted = 7;

int: clara = 12;

int: bestman = 3;

int: alice = 8;

int: ron = 9;

int: bridesmaid = 4;

int: bob = 5;

int: rona = 10;


array[INDEX_SET_pos_1] of var Seats: pos;

set of int: INDEX_SET_pos_1 = Hatreds;






solve maximize sum(h in Hatreds)(let {var Seats: p1 = pos[h1[h]]; var Seats: p2 = pos[h2[h]]; var 0..1: same = bool2int(p1 <= 6 <-> p2 <= 6)} in
	same * abs(p1 - p2) + (1 - same) * (abs(13 - p1 - p2) + 1));




