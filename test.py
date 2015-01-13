import sys
import unittest

import tests

if __name__ == '__main__':
    try:
        arg = sys.argv[1]

        if   arg == 'all':
            raise Exception()
        elif arg == 'full':
            print('Run the full test suite')
            tests = unittest.TestLoader().loadTestsFromModule(tests.test_full)
    except Exception as e:
        print(e)
        print('Running all tests')
        tests = unittest.TestLoader().discover('tests')

    test_runner = unittest.runner.TextTestRunner(verbosity=0)
    test_runner.run(tests)
