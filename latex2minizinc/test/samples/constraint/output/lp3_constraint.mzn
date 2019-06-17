array[0..numTanks] of float: full;

int: numTanks;

array[1..numTanks] of float: minTime;

array[1..numTanks] of float: maxTime;

array[0..numTanks, 0..numTanks] of float: empty;

int: numJobs;

float: perMax = sum(i in 1..numTanks)(maxTime[i]);


array[0..numTanks] of var int: Entry;

array[0..numTanks] of var int: Removal;

var int: Period;


constraint assert(numTanks > 0, "Assertion numTanks > 0 failed!");

constraint assert(numJobs > 0, "Assertion numJobs > 0 failed!");

constraint forall(i in 0..numTanks)(Entry[i] <= numJobs * perMax /\ Entry[i] >= 0);

constraint forall(i in 0..numTanks)(Removal[i] <= numJobs * perMax /\ Removal[i] >= 0);

constraint Period <= perMax /\ Period >= 0;

constraint forall(t in 0..numTanks)(Removal[t] + full[t] = Entry[floor((t + 1)) mod floor((numTanks + 1))]);

constraint forall(t in 1..numTanks)(Entry[t] + minTime[t] <= Removal[t] /\ Entry[t] + maxTime[t] >= Removal[t]);

constraint forall(t1 in 0..floor(numTanks - 1), t2 in floor(t1 + 1)..numTanks, k in 1..floor(numJobs - 1))(Entry[floor((t1 + 1)) mod floor((numTanks + 1))] + empty[floor((t1 + 1)) mod floor((numTanks + 1)),t2] <= Removal[t2] - k * Period \/ Entry[floor((t2 + 1)) mod floor((numTanks + 1))] + empty[floor((t2 + 1)) mod floor((numTanks + 1)),t1] <= Removal[t1] + k * Period);

constraint Removal[0] = 0;

constraint Removal[numTanks] + full[numTanks] <= numJobs * Period;



solve minimize Period;




