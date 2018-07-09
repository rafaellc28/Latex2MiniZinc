array[int] of float: full;

int: numTanks;

array[int] of float: minTime;

array[int] of float: maxTime;

array[int, int] of float: empty;

int: numJobs;

float: perMax = sum(i in 1..numTanks)(maxTime[i]);


array[INDEX_SET_Entry_1] of var int: Entry;

array[INDEX_SET_Removal_1] of var int: Removal;

var int: Period;

set of int: INDEX_SET_Entry_1 = 0..numTanks;

set of int: INDEX_SET_Removal_1 = 0..numTanks;


constraint assert(numTanks > 0, "Assertion numTanks > 0 failed!");

constraint assert(numJobs > 0, "Assertion numJobs > 0 failed!");

constraint forall(i in INDEX_SET_Entry_1)(Entry[i] <= numJobs * perMax /\ Entry[i] >= 0);

constraint forall(i in INDEX_SET_Removal_1)(Removal[i] <= numJobs * perMax /\ Removal[i] >= 0);

constraint Period <= perMax /\ Period >= 0;

constraint forall(t in 0..numTanks)(Removal[t] + full[t] = Entry[floor((t + 1)) mod floor((numTanks + 1))]);

constraint forall(t in 1..numTanks)(Entry[t] + minTime[t] <= Removal[t] /\ Entry[t] + maxTime[t] >= Removal[t]);

constraint forall(t1 in 0..floor(numTanks - 1), t2 in floor(t1 + 1)..numTanks, k in 1..floor(numJobs - 1))(Entry[floor((t1 + 1)) mod floor((numTanks + 1))] + empty[floor((t1 + 1)) mod floor((numTanks + 1)),t2] <= Removal[t2] - k * Period \/ Entry[floor((t2 + 1)) mod floor((numTanks + 1))] + empty[floor((t2 + 1)) mod floor((numTanks + 1)),t1] <= Removal[t1] + k * Period);

constraint Removal[0] = 0;

constraint Removal[numTanks] + full[numTanks] <= numJobs * Period;



solve minimize Period;




