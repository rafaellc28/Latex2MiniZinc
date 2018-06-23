set of int: c_final;

enum port;

array[INDEX_SET_cp_pos] of set of int: cp_pos;

enum nutr;

enum region;

array[INDEX_SET_p_pos_1] of set of int: p_pos = array1d(INDEX_SET_p_pos_1, [p_capp_diff_p_exceptp[p] | p in plant]);

enum c_ship;

array[INDEX_SET_cc_pos] of set of int: cc_pos;

set of int: c_raw;

set of int: commod = c_final union c_inter union c_raw;

enum plant;

array[INDEX_SET_m_pos] of set of int: m_pos;

enum center;

set of int: c_inter;

array[int] of set of int: p_except;

enum proc;

array[int] of set of int: p_cap;

array[INDEX_SET_c_pos_1] of set of int: c_pos = array1d(INDEX_SET_c_pos_1, [cp_posc_union_cc_posc[c] | c in commod]);

enum unit;

array[int, int] of float: fn;

array[INDEX_SET_cn75_1, INDEX_SET_cn75_2] of float: cn75 = array2d(INDEX_SET_cn75_1, INDEX_SET_cn75_2, [sum(c in c_final)(cf75[r,c] * fn[c,n]) | r in region, n in nutr]);

array[int, int] of float: cf75;

array[int, int] of float: io;

array[int] of float: p_imp;

array[INDEX_SET_p_dom_1, INDEX_SET_p_dom_2] of float: p_dom = array2d(INDEX_SET_p_dom_1, INDEX_SET_p_dom_2, [if p_r[c] > 0 then p_r[c] else p_pr[pl,c] endif | pl in plant, c in c_raw]);

array[int, int] of float: util;

float: util_pct = 0.85;

array[INDEX_SET_icap_1, INDEX_SET_icap_2] of float: icap = array2d(INDEX_SET_icap_1, INDEX_SET_icap_2, [0.33 * dcap[pl,u] | u in unit, pl in plant]);

array[INDEX_SET_tran_final_1, INDEX_SET_tran_final_2] of float: tran_final = array2d(INDEX_SET_tran_final_1, INDEX_SET_tran_final_2, [if road[r,pl] > 0 then (0.5 + 0.0144 * road[r,pl]) else 0 endif | pl in plant, r in region]);

array[INDEX_SET_tran_import_1, INDEX_SET_tran_import_2] of float: tran_import = array2d(INDEX_SET_tran_import_1, INDEX_SET_tran_import_2, [if road[r,po] > 0 then (0.5 + 0.0144 * road[r,po]) else 0 endif | r in region, po in port]);

array[INDEX_SET_tran_inter_1, INDEX_SET_tran_inter_2] of float: tran_inter = array2d(INDEX_SET_tran_inter_1, INDEX_SET_tran_inter_2, [if rail[p1,p2] > 0 then (3.5 + 0.03 * rail[p1,p2]) else 0 endif | p1 in plant, p2 in plant]);

array[INDEX_SET_tran_raw_1] of float: tran_raw = array1d(INDEX_SET_tran_raw_1, [(if impd_barg[pl] > 0 then (1.0 + 0.0030 * impd_barg[pl]) else 0 endif) + (if impd_road[pl] > 0 then (0.5 + 0.0144 * impd_road[pl]) else 0 endif) | pl in plant]);

float: exch = 0.4;

array[int, int] of float: road;

array[int] of float: impd_barg;

array[int] of float: impd_road;

array[int, int] of float: rail_half;

array[int] of float: p_r;

array[int, int] of float: p_pr;

array[int, int] of float: dcap;

array[INDEX_SET_rail_1, INDEX_SET_rail_2] of float: rail = array2d(INDEX_SET_rail_1, INDEX_SET_rail_2, [if rail_half[p1,p2] > 0 then rail_half[p1,p2] else rail_half[p2,p1] endif | p1 in plant, p2 in plant]);


array[INDEX_SET_Z_1, INDEX_SET_Z_2] of var float: Z;

array[INDEX_SET_Xf_1, INDEX_SET_Xf_2, INDEX_SET_Xf_3] of var float: Xf;

array[INDEX_SET_Xi_1, INDEX_SET_Xi_2, INDEX_SET_Xi_3] of var float: Xi;

array[INDEX_SET_Vf_1, INDEX_SET_Vf_2, INDEX_SET_Vf_3] of var float: Vf;

array[INDEX_SET_Vr_1, INDEX_SET_Vr_2] of var float: Vr;

array[INDEX_SET_U_1, INDEX_SET_U_2] of var float: U;

var float: Psip;

var float: Psil;

var float: Psii;

set of int: INDEX_SET_U_1 = c_raw;

set of int: INDEX_SET_U_2;

set of int: INDEX_SET_Vf_1 = c_final;

set of int: INDEX_SET_Vf_2 = region;

set of int: INDEX_SET_Vf_3 = port;

set of int: INDEX_SET_Vr_1 = c_raw;

set of int: INDEX_SET_Vr_2;

set of int: INDEX_SET_Xf_1 = c_final;

set of int: INDEX_SET_Xf_2;

set of int: INDEX_SET_Xf_3 = region;

set of int: INDEX_SET_Xi_1 = c_ship;

set of int: INDEX_SET_Xi_2;

set of int: INDEX_SET_Xi_3;

set of int: INDEX_SET_Z_1 = plant;

set of int: INDEX_SET_Z_2;

set of int: INDEX_SET_c_pos_1;

set of int: INDEX_SET_cc_pos;

set of int: INDEX_SET_cn75_1;

set of int: INDEX_SET_cn75_2;

set of int: INDEX_SET_cp_pos;

set of int: INDEX_SET_cp_posc_union_cc_posc;

set of int: INDEX_SET_icap_1;

set of int: INDEX_SET_icap_2;

set of int: INDEX_SET_m_pos;

set of int: INDEX_SET_p_capp_diff_p_exceptp;

set of int: INDEX_SET_p_dom_1;

set of int: INDEX_SET_p_dom_2;

set of int: INDEX_SET_p_pos_1;

set of int: INDEX_SET_rail_1;

set of int: INDEX_SET_rail_2;

set of int: INDEX_SET_tran_final_1;

set of int: INDEX_SET_tran_final_2;

set of int: INDEX_SET_tran_import_1;

set of int: INDEX_SET_tran_import_2;

set of int: INDEX_SET_tran_inter_1;

set of int: INDEX_SET_tran_inter_2;

set of int: INDEX_SET_tran_raw_1;

array[INDEX_SET_cp_posc_union_cc_posc] of int: cp_posc_union_cc_posc;

array[INDEX_SET_p_capp_diff_p_exceptp] of int: p_capp_diff_p_exceptp;


constraint forall(pl in INDEX_SET_Z_1, p in INDEX_SET_Z_2)(Z[pl,p] >= 0);

constraint forall(c in INDEX_SET_Xf_1, cp in INDEX_SET_Xf_2, r in INDEX_SET_Xf_3)(Xf[c,cp,r] >= 0);

constraint forall(c in INDEX_SET_Xi_1, cp in INDEX_SET_Xi_2, cc in INDEX_SET_Xi_3)(Xi[c,cp,cc] >= 0);

constraint forall(cf in INDEX_SET_Vf_1, r in INDEX_SET_Vf_2, p in INDEX_SET_Vf_3)(Vf[cf,r,p] >= 0);

constraint forall(c in INDEX_SET_Vr_1, cc in INDEX_SET_Vr_2)(Vr[c,cc] >= 0);

constraint forall(c in INDEX_SET_U_1, cc in INDEX_SET_U_2)(U[c,cc] >= 0);

constraint forall(n in nutr, r in region)(sum(c in c_final)(fn[c,n] * (sum(po in port)(Vf[c,r,po] + sum(pl in cp_pos[c])(Xf[c,pl,r])))) >= cn75[r,n]);

constraint forall(c in c_final, r in region where cf75[r,c] > 0)(sum(po in port)(Vf[c,r,po] + sum(pl in cp_pos[c])(Xf[c,pl,r])) >= cf75[r,c]);

constraint forall(c in commod, pl in plant)(sum(pr in p_pos[pl])(io[c,pr] * Z[pl,pr] + (if (c in c_ship) then (if pl in cp_pos[c] then sum(p2 in cc_pos[c])(Xi[c,pl,p2]) else 0 endif) - (if pl in cc_pos[c] then sum(p2 in cp_pos[c])(Xi[c,p2,pl]) else 0 endif) else 0 endif) + (if (c in c_raw /\ pl in cc_pos[c]) then ((if p_imp[c] > 0 then Vr[c,pl] else 0 endif) + (if p_dom[pl,c] > 0 then U[c,pl] else 0 endif)) else 0 endif)) >= if (c in c_final /\ pl in cp_pos[c]) then sum(r in region)(Xf[c,pl,r]) else 0 endif);

constraint forall(pl in plant, u in m_pos[pl])(sum(pr in p_pos[pl])(util[u,pr] * Z[pl,pr]) <= util_pct * icap[u,pl]);

constraint Psip = sum(c in c_raw, pl in cc_pos[c])(p_dom[pl,c] * U[c,pl]);

constraint Psil = sum(c in c_final)((sum(pl in cp_pos[c], r in region)(tran_final[pl,r] * Xf[c,pl,r] + sum(po in port, r in region)(tran_import[r,po] * Vf[c,r,po]))) + sum(c in c_ship, p1 in cp_pos[c], p2 in cc_pos[c])(tran_inter[p1,p2] * Xi[c,p1,p2] + sum(c in c_raw, pl in cc_pos[c] where p_imp[c] > 0)(tran_raw[pl] * Vr[c,pl])));

constraint Psii/exch = sum(c in c_final, r in region, po in port)(p_imp[c] * Vf[c,r,po] + sum(c in c_raw, pl in cc_pos[c])(p_imp[c] * Vr[c,pl]));



solve minimize Psip + Psil + Psii;




