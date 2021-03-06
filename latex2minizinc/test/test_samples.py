import difflib
from latex2minizinc.Compiler import *

compiler = None

def setup_module(module):
	module.compiler = Compiler()


def check_test(name1, name2):
	f1 = open(name1, 'r')
	f2 = open(name2, 'r')

	expected = f2.read()
	expected = expected[:-1] # remove last \n

	doc = f1.read()
	#compiler = Compiler()

	actual = compiler.compile(doc)

	expected=expected.splitlines(True)
	actual=actual.splitlines(True)

	diff = difflib.unified_diff(expected, actual)
	diff = list(diff)

	f1.close()
	f2.close()
	
	if len(diff) != 0:
		print(''.join(diff))
		
	assert len(diff) == 0

def check_test_num(num, with_declarations = False):
	if with_declarations:
		name1 = 'latex2minizinc/test/samples/lp'+str(num)+'_with_declarations.tex.equation'
		name2 = 'latex2minizinc/test/samples/output/lp'+str(num)+'_with_declarations.mzn'
	else:
		name1 = 'latex2minizinc/test/samples/lp'+str(num)+'.tex.equation'
		name2 = 'latex2minizinc/test/samples/output/lp'+str(num)+'.mzn'

	check_test(name1, name2)

def check_test_nonlinear_num(num, with_declarations = False):
	if with_declarations:
		name1 = 'latex2minizinc/test/samples/nonlinear/lp'+str(num)+'_nonlinear_with_declarations.tex.equation'
		name2 = 'latex2minizinc/test/samples/nonlinear/output/lp'+str(num)+'_nonlinear_with_declarations.mzn'
	else:
		name1 = 'latex2minizinc/test/samples/nonlinear/lp'+str(num)+'_nonlinear.tex.equation'
		name2 = 'latex2minizinc/test/samples/nonlinear/output/lp'+str(num)+'_nonlinear.mzn'

	check_test(name1, name2)

def check_test_linear_num(num, with_declarations = False):
	if with_declarations:
		name1 = 'latex2minizinc/test/samples/linear/lp'+str(num)+'_linear_with_declarations.tex.equation'
		name2 = 'latex2minizinc/test/samples/linear/output/lp'+str(num)+'_linear_with_declarations.mzn'
	else:
		name1 = 'latex2minizinc/test/samples/linear/lp'+str(num)+'_linear.tex.equation'
		name2 = 'latex2minizinc/test/samples/linear/output/lp'+str(num)+'_linear.mzn'

	check_test(name1, name2)

def check_test_constraint_num(num, with_declarations = False):
	if with_declarations:
		name1 = 'latex2minizinc/test/samples/constraint/lp'+str(num)+'_constraint_with_declarations.tex.equation'
		name2 = 'latex2minizinc/test/samples/constraint/output/lp'+str(num)+'_constraint_with_declarations.mzn'
	else:
		name1 = 'latex2minizinc/test/samples/constraint/lp'+str(num)+'_constraint.tex.equation'
		name2 = 'latex2minizinc/test/samples/constraint/output/lp'+str(num)+'_constraint.mzn'

	check_test(name1, name2)

def check_test_extras_num(num):
	name1 = 'latex2minizinc/test/samples/extras/test'+str(num)+'.tex.equation'
	name2 = 'latex2minizinc/test/samples/extras/output/test'+str(num)+'.mzn'

	check_test(name1, name2)

def check_test_minizinc_num(num):
	name1 = 'latex2minizinc/test/samples/minizinc/minizinc'+str(num)+'.tex.equation'
	name2 = 'latex2minizinc/test/samples/minizinc/output/minizinc'+str(num)+'.mzn'

	check_test(name1, name2)

def test_lp0():
	check_test_num(0)

def test_lp0_with_declarations():
	check_test_num(0, True)

def test_lp1():
	check_test_num(1)

def test_lp1_with_declarations():
	check_test_num(1, True)

def test_lp2():
	check_test_num(2)

def test_lp2_with_declarations():
	check_test_num(2, True)

def test_lp3():
	check_test_num(3)

def test_lp3_with_declarations():
	check_test_num(3, True)

def test_lp4():
	check_test_num(4)

def test_lp4_with_declarations():
	check_test_num(4, True)

def test_lp5():
	check_test_num(5)

def test_lp5_with_declarations():
	check_test_num(5, True)

def test_lp6():
	check_test_num(6)

def test_lp6_with_declarations():
	check_test_num(6, True)

def test_lp7():
	check_test_num(7)

def test_lp7_with_declarations():
	check_test_num(7, True)

def test_lp8():
	check_test_num(8)

def test_lp8_with_declarations():
	check_test_num(8, True)

def test_lp9():
	check_test_num(9)

def test_lp9_with_declarations():
	check_test_num(9, True)



def test_lp10():
	check_test_num(10)

def test_lp10_with_declarations():
	check_test_num(10, True)


def test_lp11():
	check_test_num(11)

def test_lp11_with_declarations():
	check_test_num(11, True)

def test_lp12():
	check_test_num(12)

def test_lp12_with_declarations():
	check_test_num(12, True)


def test_lp13():
	check_test_num(13)

def test_lp13_with_declarations():
	check_test_num(13, True)

def test_lp14():
	check_test_num(14)

def test_lp14_with_declarations():
	check_test_num(14, True)

def test_lp15():
	check_test_num(15)

def test_lp15_with_declarations():
	check_test_num(15, True)


def test_lp16():
	check_test_num(16)

def test_lp16_with_declarations():
	check_test_num(16, True)

def test_lp17():
	check_test_num(17)

def test_lp17_with_declarations():
	check_test_num(17, True)

def test_lp18():
	check_test_num(18)

def test_lp18_with_declarations():
	check_test_num(18, True)

def test_lp19():
	check_test_num(19)

def test_lp19_with_declarations():
	check_test_num(19, True)



def test_lp20():
	check_test_num(20)

def test_lp20_with_declarations():
	check_test_num(20, True)

def test_lp21():
	check_test_num(21)

def test_lp21_with_declarations():
	check_test_num(21, True)

def test_lp22():
	check_test_num(22)

def test_lp22_with_declarations():
	check_test_num(22, True)

def test_lp23():
	check_test_num(23)

def test_lp23_with_declarations():
	check_test_num(23, True)

def test_lp24():
	check_test_num(24)

def test_lp24_with_declarations():
	check_test_num(24, True)

def test_lp25():
	check_test_num(25)

def test_lp25_with_declarations():
	check_test_num(25, True)

def test_lp26():
	check_test_num(26)

def test_lp26_with_declarations():
	check_test_num(26, True)

def test_lp27():
	check_test_num(27)

def test_lp27_with_declarations():
	check_test_num(27, True)

def test_lp28():
	check_test_num(28)

def test_lp28_with_declarations():
	check_test_num(28, True)

def test_lp29():
	check_test_num(29)

def test_lp29_with_declarations():
	check_test_num(29, True)


def test_lp30():
	check_test_num(30)

def test_lp30_with_declarations():
	check_test_num(30, True)

def test_lp31():
	check_test_num(31)

def test_lp31_with_declarations():
	check_test_num(31, True)

def test_lp32():
	check_test_num(32)

def test_lp32_with_declarations():
	check_test_num(32, True)

def test_lp33():
	check_test_num(33)

def test_lp33_with_declarations():
	check_test_num(33, True)

def test_lp34():
	check_test_num(34)

def test_lp34_with_declarations():
	check_test_num(34, True)

def test_lp35():
	check_test_num(35)

def test_lp35_with_declarations():
	check_test_num(35, True)

def test_lp36():
	check_test_num(36)

def test_lp36_with_declarations():
	check_test_num(36, True)

def test_lp37():
	check_test_num(37)

def test_lp37_with_declarations():
	check_test_num(37, True)

def test_lp38():
	check_test_num(38)

def test_lp38_with_declarations():
	check_test_num(38, True)

'''
def test_lp39():
	check_test_num(39)

def test_lp39_with_declarations():
	check_test_num(39, True)
'''

def test_lp40():
	check_test_num(40)

def test_lp40_with_declarations():
	check_test_num(40, True)

def test_lp41():
	check_test_num(41)

def test_lp41_with_declarations():
	check_test_num(41, True)

def test_lp42():
	check_test_num(42)

def test_lp42_with_declarations():
	check_test_num(42, True)

def test_lp43():
	check_test_num(43)

def test_lp43_with_declarations():
	check_test_num(43, True)

def test_lp44():
	check_test_num(44)

def test_lp44_with_declarations():
	check_test_num(44, True)

def test_lp45():
	check_test_num(45)

def test_lp45_with_declarations():
	check_test_num(45, True)

def test_lp46():
	check_test_num(46)

def test_lp46_with_declarations():
	check_test_num(46, True)

def test_lp47():
	check_test_num(47)

def test_lp47_with_declarations():
	check_test_num(47, True)

def test_lp48():
	check_test_num(48)

def test_lp48_with_declarations():
	check_test_num(48, True)

def test_lp49():
	check_test_num(49)

def test_lp49_with_declarations():
	check_test_num(49, True)


def test_lp50():
	check_test_num(50)

def test_lp50_with_declarations():
	check_test_num(50, True)

def test_lp51():
	check_test_num(51)

def test_lp51_with_declarations():
	check_test_num(51, True)

def test_lp52():
	check_test_num(52)

def test_lp52_with_declarations():
	check_test_num(52, True)

def test_lp53():
	check_test_num(53)

def test_lp53_with_declarations():
	check_test_num(53, True)

def test_lp54():
	check_test_num(54)

def test_lp54_with_declarations():
	check_test_num(54, True)

def test_lp55():
	check_test_num(55)

def test_lp55_with_declarations():
	check_test_num(55, True)

def test_lp56():
	check_test_num(56)

def test_lp56_with_declarations():
	check_test_num(56, True)

def test_lp57():
	check_test_num(57)

def test_lp57_with_declarations():
	check_test_num(57, True)

def test_lp58():
	check_test_num(58)

def test_lp58_with_declarations():
	check_test_num(58, True)

def test_lp59():
	check_test_num(59)

def test_lp59_with_declarations():
	check_test_num(59, True)


def test_lp60():
	check_test_num(60)

def test_lp60_with_declarations():
	check_test_num(60, True)

def test_lp61():
	check_test_num(61)

def test_lp61_with_declarations():
	check_test_num(61, True)

def test_lp62():
	check_test_num(62)

def test_lp62_with_declarations():
	check_test_num(62, True)

def test_lp63():
	check_test_num(63)

def test_lp63_with_declarations():
	check_test_num(63, True)

'''
def test_lp64():
	check_test_num(64)

def test_lp64_with_declarations():
	check_test_num(64, True)
'''

def test_lp65():
	check_test_num(65)

def test_lp65_with_declarations():
	check_test_num(65, True)

'''
def test_lp66():
	check_test_num(66)

def test_lp66_with_declarations():
	check_test_num(66, True)
'''

def test_lp67():
	check_test_num(67)

def test_lp67_with_declarations():
	check_test_num(67, True)

def test_lp68():
	check_test_num(68)

def test_lp68_with_declarations():
	check_test_num(68, True)

def test_lp69():
	check_test_num(69)

def test_lp69_with_declarations():
	check_test_num(69, True)


def test_lp70():
	check_test_num(70)

def test_lp70_with_declarations():
	check_test_num(70, True)

def test_lp71_with_declarations():
	check_test_num(71, True)

def test_lp72_with_declarations():
	check_test_num(72, True)

def test_lp73_with_declarations():
	check_test_num(73, True)

'''
def test_lp74_with_declarations():
	check_test_num(74, True)

def test_lp75_with_declarations():
	check_test_num(75, True)
'''

def test_lp76_with_declarations():
	check_test_num(76, True)


# Nonlinear Programming
def test_lp0_nonlinear():
	check_test_nonlinear_num(0)

def test_lp1_nonlinear():
	check_test_nonlinear_num(1)

def test_lp2_nonlinear():
	check_test_nonlinear_num(2)

def test_lp3_nonlinear():
	check_test_nonlinear_num(3)

def test_lp4_nonlinear():
	check_test_nonlinear_num(4)

def test_lp5_nonlinear():
	check_test_nonlinear_num(5)

def test_lp6_nonlinear():
	check_test_nonlinear_num(6)

def test_lp7_nonlinear():
	check_test_nonlinear_num(7)

def test_lp8_nonlinear():
	check_test_nonlinear_num(8)

def test_lp9_nonlinear():
	check_test_nonlinear_num(9)

def test_lp10_nonlinear():
	check_test_nonlinear_num(10)

def test_lp11_nonlinear():
	check_test_nonlinear_num(11)

def test_lp12_nonlinear():
	check_test_nonlinear_num(12)

def test_lp13_nonlinear():
	check_test_nonlinear_num(13)

def test_lp14_nonlinear():
	check_test_nonlinear_num(14)

def test_lp15_nonlinear():
	check_test_nonlinear_num(15)

def test_lp16_nonlinear():
	check_test_nonlinear_num(16)

def test_lp17_nonlinear():
	check_test_nonlinear_num(17)

def test_lp18_nonlinear():
	check_test_nonlinear_num(18)

def test_lp19_nonlinear():
	check_test_nonlinear_num(19)

def test_lp20_nonlinear():
	check_test_nonlinear_num(20)

def test_lp21_nonlinear():
	check_test_nonlinear_num(21)

def test_lp22_nonlinear():
	check_test_nonlinear_num(22)

def test_lp23_nonlinear():
	check_test_nonlinear_num(23)

def test_lp24_nonlinear():
	check_test_nonlinear_num(24)

def test_lp25_nonlinear():
	check_test_nonlinear_num(25)

def test_lp26_nonlinear():
	check_test_nonlinear_num(26)

def test_lp27_nonlinear():
	check_test_nonlinear_num(27)

def test_lp28_nonlinear():
	check_test_nonlinear_num(28)

def test_lp29_nonlinear():
	check_test_nonlinear_num(29)

def test_lp30_nonlinear():
	check_test_nonlinear_num(30)

def test_lp31_nonlinear():
	check_test_nonlinear_num(31)

def test_lp32_nonlinear():
	check_test_nonlinear_num(32)

def test_lp33_nonlinear():
	check_test_nonlinear_num(33)

def test_lp34_nonlinear():
	check_test_nonlinear_num(34)

def test_lp35_nonlinear():
	check_test_nonlinear_num(35)

def test_lp36_nonlinear():
	check_test_nonlinear_num(36)


# Constraint Programming
def test_lp0_constraint():
	check_test_constraint_num(0)

def test_lp1_constraint():
	check_test_constraint_num(1)

def test_lp2_constraint():
	check_test_constraint_num(2)

def test_lp3_constraint():
	check_test_constraint_num(3)


# Extras
def test_extras_test1():
	check_test_extras_num(1)

def test_extras_test2():
	check_test_extras_num(2)

def test_extras_test3():
	check_test_extras_num(3)

def test_extras_test4():
	check_test_extras_num(4)

def test_extras_test5():
	check_test_extras_num(5)

def test_extras_test6():
	check_test_extras_num(6)

def test_extras_test7():
	check_test_extras_num(7)

def test_extras_test8():
	check_test_extras_num(8)

def test_extras_test9():
	check_test_extras_num(9)

def test_extras_test10():
	check_test_extras_num(10)

def test_extras_test11():
	check_test_extras_num(11)

def test_extras_test12():
	check_test_extras_num(12)

def test_extras_test13():
	check_test_extras_num(13)

def test_extras_test14():
	check_test_extras_num(14)

def test_extras_test15():
	check_test_extras_num(15)

def test_extras_test16():
	check_test_extras_num(16)

def test_extras_test17():
	check_test_extras_num(17)

def test_extras_test18():
	check_test_extras_num(18)

def test_extras_test19():
	check_test_extras_num(19)

def test_extras_test20():
	check_test_extras_num(20)

def test_extras_test21():
	check_test_extras_num(21)

def test_extras_test22():
	check_test_extras_num(22)

def test_extras_test23():
	check_test_extras_num(23)

def test_extras_test24():
	check_test_extras_num(24)

def test_extras_test25():
	check_test_extras_num(25)

def test_extras_test26():
	check_test_extras_num(26)

def test_extras_test27():
	check_test_extras_num(27)

def test_extras_test28():
	check_test_extras_num(28)

def test_extras_test29():
	check_test_extras_num(29)

def test_extras_test30():
	check_test_extras_num(30)

def test_extras_test31():
	check_test_extras_num(31)

def test_extras_test32():
	check_test_extras_num(32)

def test_extras_test33():
	check_test_extras_num(33)

def test_extras_test34():
	check_test_extras_num(34)

def test_extras_test35():
	check_test_extras_num(35)

def test_extras_test36():
	check_test_extras_num(36)

def test_extras_test37():
	check_test_extras_num(37)

def test_extras_test38():
	check_test_extras_num(38)

def test_extras_test39():
	check_test_extras_num(39)

def test_extras_test40():
	check_test_extras_num(40)

def test_extras_test41():
	check_test_extras_num(41)

def test_extras_test42():
	check_test_extras_num(42)

def test_extras_test43():
	check_test_extras_num(43)

def test_extras_test44():
	check_test_extras_num(44)

def test_extras_test45():
	check_test_extras_num(45)

def test_extras_test46():
	check_test_extras_num(46)

def test_extras_test47():
	check_test_extras_num(47)

def test_extras_test48():
	check_test_extras_num(48)

def test_extras_test49():
	check_test_extras_num(49)

def test_extras_test50():
	check_test_extras_num(50)

def test_extras_test51():
	check_test_extras_num(51)

def test_extras_test52():
	check_test_extras_num(52)

def test_extras_test53():
	check_test_extras_num(53)

def test_extras_test54():
	check_test_extras_num(54)

def test_extras_test55():
	check_test_extras_num(55)

def test_extras_test56():
	check_test_extras_num(56)

def test_extras_test57():
	check_test_extras_num(57)

def test_extras_test58():
	check_test_extras_num(58)

def test_extras_test59():
	check_test_extras_num(59)

def test_extras_test60():
	check_test_extras_num(60)

def test_extras_test61():
	check_test_extras_num(61)

def test_extras_test62():
	check_test_extras_num(62)

def test_extras_test63():
	check_test_extras_num(63)

def test_extras_test64():
	check_test_extras_num(64)

def test_extras_test65():
	check_test_extras_num(65)

def test_extras_test66():
	check_test_extras_num(66)

def test_extras_test67():
	check_test_extras_num(67)

def test_extras_test68():
	check_test_extras_num(68)

def test_extras_test69():
	check_test_extras_num(69)

def test_extras_test70():
	check_test_extras_num(70)

def test_extras_test71():
	check_test_extras_num(71)

def test_extras_test72():
	check_test_extras_num(72)

def test_extras_test73():
	check_test_extras_num(73)

def test_extras_test74():
	check_test_extras_num(74)

def test_extras_test75():
	check_test_extras_num(75)

def test_extras_test76():
	check_test_extras_num(76)

def test_extras_test77():
	check_test_extras_num(77)

def test_extras_test78():
	check_test_extras_num(78)

def test_extras_test79():
	check_test_extras_num(79)

def test_extras_test80():
	check_test_extras_num(80)

def test_extras_test81():
	check_test_extras_num(81)

def test_extras_test82():
	check_test_extras_num(82)

def test_extras_test83():
	check_test_extras_num(83)

def test_extras_test84():
	check_test_extras_num(84)

def test_extras_test85():
	check_test_extras_num(85)

def test_extras_test86():
	check_test_extras_num(86)

def test_extras_test87():
	check_test_extras_num(87)

def test_extras_test86():
	check_test_extras_num(86)

def test_extras_test87():
	check_test_extras_num(87)

def test_extras_test88():
	check_test_extras_num(88)

def test_extras_test89():
	check_test_extras_num(89)

def test_extras_test90():
	check_test_extras_num(90)

def test_extras_test91():
	check_test_extras_num(91)

def test_extras_test92():
	check_test_extras_num(92)

def test_extras_test93():
	check_test_extras_num(93)

def test_extras_test94():
	check_test_extras_num(94)

def test_extras_test95():
	check_test_extras_num(95)

def test_extras_test96():
	check_test_extras_num(96)

def test_extras_test97():
	check_test_extras_num(97)

def test_extras_test98():
	check_test_extras_num(98)

# MiniZinc
def test_minizinc_test0():
	check_test_minizinc_num(0)

def test_minizinc_test1():
	check_test_minizinc_num(1)

def test_minizinc_test2():
	check_test_minizinc_num(2)

def test_minizinc_test3():
	check_test_minizinc_num(3)

def test_minizinc_test4():
	check_test_minizinc_num(4)

def test_minizinc_test5():
	check_test_minizinc_num(5)

def test_minizinc_test6():
	check_test_minizinc_num(6)

def test_minizinc_test7():
	check_test_minizinc_num(7)

def test_minizinc_test8():
	check_test_minizinc_num(8)

def test_minizinc_test9():
	check_test_minizinc_num(9)

def test_minizinc_test10():
	check_test_minizinc_num(10)

def test_minizinc_test11():
	check_test_minizinc_num(11)

def test_minizinc_test12():
	check_test_minizinc_num(12)

def test_minizinc_test13():
	check_test_minizinc_num(13)

def test_minizinc_test14():
	check_test_minizinc_num(14)

def test_minizinc_test15():
	check_test_minizinc_num(15)

def test_minizinc_test16():
	check_test_minizinc_num(16)

def test_minizinc_test17():
	check_test_minizinc_num(17)

def test_minizinc_test18():
	check_test_minizinc_num(18)

def test_minizinc_test19():
	check_test_minizinc_num(19)

def test_minizinc_test20():
	check_test_minizinc_num(20)

def test_minizinc_test21():
	check_test_minizinc_num(21)

def test_minizinc_test22():
	check_test_minizinc_num(22)

def test_minizinc_test23():
	check_test_minizinc_num(23)

def test_minizinc_test24():
	check_test_minizinc_num(24)

def test_minizinc_test25():
	check_test_minizinc_num(25)

def test_minizinc_test26():
	check_test_minizinc_num(26)

def test_minizinc_test27():
	check_test_minizinc_num(27)

def test_minizinc_test28():
	check_test_minizinc_num(28)

def test_minizinc_test29():
	check_test_minizinc_num(29)

def test_minizinc_test30():
	check_test_minizinc_num(30)

def test_minizinc_test31():
	check_test_minizinc_num(31)

def test_minizinc_test32():
	check_test_minizinc_num(32)

def test_minizinc_test33():
	check_test_minizinc_num(33)

def test_minizinc_test34():
	check_test_minizinc_num(34)

def test_minizinc_test35():
	check_test_minizinc_num(35)

def test_minizinc_test36():
	check_test_minizinc_num(36)

def test_minizinc_test37():
	check_test_minizinc_num(37)

def test_minizinc_test38():
	check_test_minizinc_num(38)

def test_minizinc_test39():
	check_test_minizinc_num(39)

def test_minizinc_test40():
	check_test_minizinc_num(40)

def test_minizinc_test41():
	check_test_minizinc_num(41)

def test_minizinc_test42():
	check_test_minizinc_num(42)

def test_minizinc_test43():
	check_test_minizinc_num(43)

def test_minizinc_test44():
	check_test_minizinc_num(44)

def test_minizinc_test45():
	check_test_minizinc_num(45)

def test_minizinc_test46():
	check_test_minizinc_num(46)

def test_minizinc_test47():
	check_test_minizinc_num(47)

def test_minizinc_test48():
	check_test_minizinc_num(48)

def test_minizinc_test49():
	check_test_minizinc_num(49)

def test_minizinc_test50():
	check_test_minizinc_num(50)

def test_minizinc_test51():
	check_test_minizinc_num(51)

def test_minizinc_test52():
	check_test_minizinc_num(52)

def test_minizinc_test53():
	check_test_minizinc_num(53)

def test_minizinc_test54():
	check_test_minizinc_num(54)

def test_minizinc_test55():
	check_test_minizinc_num(55)

def test_minizinc_test56():
	check_test_minizinc_num(56)

def test_minizinc_test57():
	check_test_minizinc_num(57)

def test_minizinc_test58():
	check_test_minizinc_num(58)

def test_minizinc_test59():
	check_test_minizinc_num(59)

def test_minizinc_test60():
	check_test_minizinc_num(60)

def test_minizinc_test61():
	check_test_minizinc_num(61)

def test_minizinc_test62():
	check_test_minizinc_num(62)

def test_minizinc_test63():
	check_test_minizinc_num(63)

def test_minizinc_test64():
	check_test_minizinc_num(64)

def test_minizinc_test65():
	check_test_minizinc_num(65)

def test_minizinc_test66():
	check_test_minizinc_num(66)

def test_minizinc_test67():
	check_test_minizinc_num(67)

def test_minizinc_test68():
	check_test_minizinc_num(68)

def test_minizinc_test69():
	check_test_minizinc_num(69)

def test_minizinc_test70():
	check_test_minizinc_num(70)

def test_minizinc_test71():
	check_test_minizinc_num(71)

def test_minizinc_test72():
	check_test_minizinc_num(72)

def test_minizinc_test73():
	check_test_minizinc_num(73)

def test_minizinc_test74():
	check_test_minizinc_num(74)

def test_minizinc_test75():
	check_test_minizinc_num(75)

def test_minizinc_test76():
	check_test_minizinc_num(76)

def test_minizinc_test77():
	check_test_minizinc_num(77)

def test_minizinc_test78():
	check_test_minizinc_num(78)

def test_minizinc_test79():
	check_test_minizinc_num(79)

def test_minizinc_test80():
	check_test_minizinc_num(80)

def test_minizinc_test81():
	check_test_minizinc_num(81)

def test_minizinc_test82():
	check_test_minizinc_num(82)

def test_minizinc_test83():
	check_test_minizinc_num(83)

def test_minizinc_test84():
	check_test_minizinc_num(84)

def test_minizinc_test85():
	check_test_minizinc_num(85)

def test_minizinc_test86():
	check_test_minizinc_num(86)

def test_minizinc_test87():
	check_test_minizinc_num(87)

def test_minizinc_test88():
	check_test_minizinc_num(88)

def test_minizinc_test89():
	check_test_minizinc_num(89)

def test_minizinc_test90():
	check_test_minizinc_num(90)

def test_minizinc_test91():
	check_test_minizinc_num(91)

def test_minizinc_test92():
	check_test_minizinc_num(92)

def test_minizinc_test93():
	check_test_minizinc_num(93)

def test_minizinc_test94():
	check_test_minizinc_num(94)

def test_minizinc_test95():
	check_test_minizinc_num(95)

def test_minizinc_test96():
	check_test_minizinc_num(96)

def test_minizinc_test97():
	check_test_minizinc_num(97)

def test_minizinc_test98():
	check_test_minizinc_num(98)

def test_minizinc_test99():
	check_test_minizinc_num(99)

def test_minizinc_test100():
	check_test_minizinc_num(100)

def test_minizinc_test101():
	check_test_minizinc_num(101)

def test_minizinc_test102():
	check_test_minizinc_num(102)

def test_minizinc_test103():
	check_test_minizinc_num(103)

def test_minizinc_test104():
	check_test_minizinc_num(104)

def test_minizinc_test105():
	check_test_minizinc_num(105)

def test_minizinc_test106():
	check_test_minizinc_num(106)

def test_minizinc_test107():
	check_test_minizinc_num(107)

def test_minizinc_test108():
	check_test_minizinc_num(108)

def test_minizinc_test109():
	check_test_minizinc_num(109)

def test_minizinc_test110():
	check_test_minizinc_num(110)

def test_minizinc_test111():
	check_test_minizinc_num(111)

def test_minizinc_test112():
	check_test_minizinc_num(112)

def test_minizinc_test113():
	check_test_minizinc_num(113)

def test_minizinc_test114():
	check_test_minizinc_num(114)

def test_minizinc_test115():
	check_test_minizinc_num(115)

def test_minizinc_test116():
	check_test_minizinc_num(116)

def test_minizinc_test117():
	check_test_minizinc_num(117)

def test_minizinc_test118():
	check_test_minizinc_num(118)

def test_minizinc_test119():
	check_test_minizinc_num(119)

def test_minizinc_test120():
	check_test_minizinc_num(120)

def test_minizinc_test121():
	check_test_minizinc_num(121)

def test_minizinc_test122():
	check_test_minizinc_num(122)

def test_minizinc_test123():
	check_test_minizinc_num(123)

def test_minizinc_test124():
	check_test_minizinc_num(124)

def test_minizinc_test125():
	check_test_minizinc_num(125)

def test_minizinc_test126():
	check_test_minizinc_num(126)

def test_minizinc_test127():
	check_test_minizinc_num(127)

def test_minizinc_test128():
	check_test_minizinc_num(128)

def test_minizinc_test129():
	check_test_minizinc_num(129)

def test_minizinc_test130():
	check_test_minizinc_num(130)

def test_minizinc_test131():
	check_test_minizinc_num(131)

def test_minizinc_test132():
	check_test_minizinc_num(132)

def test_minizinc_test133():
	check_test_minizinc_num(133)

def test_minizinc_test134():
	check_test_minizinc_num(134)

def test_minizinc_test135():
	check_test_minizinc_num(135)

def test_minizinc_test136():
	check_test_minizinc_num(136)

def test_minizinc_test137():
	check_test_minizinc_num(137)

def test_minizinc_test138():
	check_test_minizinc_num(138)

def test_minizinc_test139():
	check_test_minizinc_num(139)

def test_minizinc_test140():
	check_test_minizinc_num(140)

def test_minizinc_test141():
	check_test_minizinc_num(141)

def test_minizinc_test142():
	check_test_minizinc_num(142)

def test_minizinc_test143():
	check_test_minizinc_num(143)

def test_minizinc_test144():
	check_test_minizinc_num(144)

def test_minizinc_test145():
	check_test_minizinc_num(145)

def test_minizinc_test146():
	check_test_minizinc_num(146)

def test_minizinc_test147():
	check_test_minizinc_num(147)

def test_minizinc_test148():
	check_test_minizinc_num(148)

def test_minizinc_test149():
	check_test_minizinc_num(149)

def test_minizinc_test150():
	check_test_minizinc_num(150)

def test_minizinc_test151():
	check_test_minizinc_num(151)

def test_minizinc_test152():
	check_test_minizinc_num(152)

def test_minizinc_test153():
	check_test_minizinc_num(153)

def test_minizinc_test154():
	check_test_minizinc_num(154)

def test_minizinc_test155():
	check_test_minizinc_num(155)

def test_minizinc_test156():
	check_test_minizinc_num(156)

def test_minizinc_test157():
	check_test_minizinc_num(157)

def test_minizinc_test158():
	check_test_minizinc_num(158)

def test_minizinc_test159():
	check_test_minizinc_num(159)

def test_minizinc_test160():
	check_test_minizinc_num(160)

def test_minizinc_test161():
	check_test_minizinc_num(161)

def test_minizinc_test162():
	check_test_minizinc_num(162)

def test_minizinc_test163():
	check_test_minizinc_num(163)

def test_minizinc_test164():
	check_test_minizinc_num(164)

def test_minizinc_test165():
	check_test_minizinc_num(165)

def test_minizinc_test166():
	check_test_minizinc_num(166)

def test_minizinc_test167():
	check_test_minizinc_num(167)

def test_minizinc_test168():
	check_test_minizinc_num(168)

def test_minizinc_test169():
	check_test_minizinc_num(169)

def test_minizinc_test170():
	check_test_minizinc_num(170)

def test_minizinc_test171():
	check_test_minizinc_num(171)

def test_minizinc_test172():
	check_test_minizinc_num(172)

def test_minizinc_test173():
	check_test_minizinc_num(173)

def test_minizinc_test174():
	check_test_minizinc_num(174)

def test_minizinc_test175():
	check_test_minizinc_num(175)

def test_minizinc_test176():
	check_test_minizinc_num(176)

def test_minizinc_test177():
	check_test_minizinc_num(177)

def test_minizinc_test178():
	check_test_minizinc_num(178)

def test_minizinc_test179():
	check_test_minizinc_num(179)

def test_minizinc_test180():
	check_test_minizinc_num(180)

def test_minizinc_test181():
	check_test_minizinc_num(181)

def test_minizinc_test182():
	check_test_minizinc_num(182)

def test_minizinc_test183():
	check_test_minizinc_num(183)

def test_minizinc_test184():
	check_test_minizinc_num(184)

def test_minizinc_test185():
	check_test_minizinc_num(185)

def test_minizinc_test186():
	check_test_minizinc_num(186)

def test_minizinc_test187():
	check_test_minizinc_num(187)

# Linear Programming
def test_lp0_linear():
	check_test_linear_num(0)

def test_lp1_linear():
	check_test_linear_num(1)

def test_lp2_linear():
	check_test_linear_num(2)

def test_lp3_linear():
	check_test_linear_num(3)

def test_lp4_linear():
	check_test_linear_num(4)

def test_lp5_linear():
	check_test_linear_num(5)

def test_lp6_linear():
	check_test_linear_num(6)

def test_lp7_linear():
	check_test_linear_num(7)

def test_lp8_linear():
	check_test_linear_num(8)

def test_lp9_linear():
	check_test_linear_num(9)

def test_lp10_linear():
	check_test_linear_num(10)

def test_lp11_linear():
	check_test_linear_num(11)

def test_lp12_linear():
	check_test_linear_num(12)

def test_lp13_linear():
	check_test_linear_num(13)

def test_lp14_linear():
	check_test_linear_num(14)

def test_lp15_linear():
	check_test_linear_num(15)

def test_lp16_linear():
	check_test_linear_num(16)

def test_lp17_linear():
	check_test_linear_num(17)

def test_lp18_linear():
	check_test_linear_num(18)

def test_lp19_linear():
	check_test_linear_num(19)

def test_lp20_linear():
	check_test_linear_num(20)

def test_lp21_linear():
	check_test_linear_num(21)

def test_lp22_linear():
	check_test_linear_num(22)

def test_lp23_linear():
	check_test_linear_num(23)

def test_lp24_linear():
	check_test_linear_num(24)

def test_lp25_linear():
	check_test_linear_num(25)

def test_lp26_linear():
	check_test_linear_num(26)

def test_lp27_linear():
	check_test_linear_num(27)

def test_lp28_linear():
	check_test_linear_num(28)

def test_lp29_linear():
	check_test_linear_num(29)

def test_lp30_linear():
	check_test_linear_num(30)

def test_lp31_linear():
	check_test_linear_num(31)

def test_lp32_linear():
	check_test_linear_num(32)

def test_lp33_linear():
	check_test_linear_num(33)

def test_lp34_linear():
	check_test_linear_num(34)

def test_lp35_linear():
	check_test_linear_num(35)

def test_lp36_linear():
	check_test_linear_num(36)

def test_lp37_linear():
	check_test_linear_num(37)

def test_lp38_linear():
	check_test_linear_num(38)

def test_lp39_linear():
	check_test_linear_num(39)

def test_lp40_linear():
	check_test_linear_num(40)

def test_lp41_linear():
	check_test_linear_num(41)

def test_lp42_linear():
	check_test_linear_num(42)

def test_lp43_linear():
	check_test_linear_num(43)

def test_lp44_linear():
	check_test_linear_num(44)

def test_lp45_linear():
	check_test_linear_num(45)

def test_lp46_linear():
	check_test_linear_num(46)

def test_lp47_linear():
	check_test_linear_num(47)

def test_lp48_linear():
	check_test_linear_num(48)

def test_lp49_linear():
	check_test_linear_num(49)

def test_lp50_linear():
	check_test_linear_num(50)

def test_lp51_linear():
	check_test_linear_num(51)
