import setuptools

if __name__ == '__main__':
	setuptools.setup(
		name='Latex to Minizinc',

		packages=setuptools.find_packages(),
		
		entry_points={
			'console_scripts': [
				'latex2minizinc = latex2minizinc.main:main',
			],
		},
		
		setup_requires=['pytest-runner', 'ply'],
		tests_require=['pytest'],
	)