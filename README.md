# 479TermProject
## Run Example Instructions
To run execute in root directory the following command:
. ./setup.sh && python3 synthesis/index.py 'path/to/code/to/modify.py' 'path/to/test/to/run.py'

Creating Example:
In unit test suite add basic performance test you wish to measure against and name the test 'perf_test' this will allow the program to identifiy and modify the test by adding more complex inputs.

Examples:
'. ./setup.sh && python3 synthesis/index.py test/sampleExecutions/sampleStructures/list.py test/sampleExecutions/test_list.py'
'. ./setup.sh && python3 synthesis/index.py test/sampleExecutions/sampleStructures/dict.py test/sampleExecutions/test_dict.py'
