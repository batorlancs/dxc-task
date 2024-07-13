import pytest
import json
from typing import Dict, List

tests: Dict[str, List[str]] = {
    'permissions': [
        'test_permission_single.py',
        'test_permission_single_leadingslash.py',
        'test_permission_all.py',
        'test_permission_none.py'
    ],
    'main': [
        'test_api_response.py'
    ]
}


def run_all_tests():
    
    tests_failed = {}
    tests_failed_count = 0
    tests_result = {}
    
    for test_group, test_files in tests.items():
        for test_file in test_files:
            if test_group == 'main':
                res = pytest.main(["-v", f"tests/{test_file}", "--tb=no"])
            else:
                res = pytest.main(["-v", f"tests/{test_group}/{test_file}"])
            if res != 0:
                if test_group not in tests_failed:
                    tests_failed[test_group] = []
                tests_failed[test_group].append(test_file)
                tests_failed_count += 1
            
            print(f"Group: {test_group}, File: {test_file}, Result: {'Failed' if res != 0 else 'Passed'}")
            
            if test_group not in tests_result:
                tests_result[test_group] = {}
            
            tests_result[test_group][test_file] = "Failed" if res != 0 else "Passed"
            
            
    print("\n\n\n------ FINAL RESULTS ------\n")
            
    if tests_failed_count > 0:
        print("\033[91mSome tests failed\033[0m")
        print(f"\033[91mNumber of Tests Failed: {tests_failed_count}\033[0m")
        print(f"\033[91mNumber of Test Groups Failed: {len(tests_failed)}\033[0m")
        print("\n\033[91mTests Failed:\033[0m")
        print("\033[91m" + json.dumps(tests_failed, indent=4) + "\033[0m")
    else:
        print("\033[92mAll tests passed\033[0m")
    
    print("\nTest Results:")
    print(json.dumps(tests_result, indent=4))
        
    
if __name__ == "__main__":
    run_all_tests()