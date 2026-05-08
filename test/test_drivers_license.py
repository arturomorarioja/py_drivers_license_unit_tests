import pytest
import sys
from app.drivers_license import drivers_license_exam_evaluation

class TestDriversLicense():

    #
    # Positive testing
    #

    @pytest.mark.parametrize('theory_exam_points, practical_exam_errors, output', [
        
        #
        # Decision table-based test cases
        #

        (90, 1, {                               # Test case 1 based on business rule 1
            'license_granted': True,
            'repeat_theory_exam': False,
            'repeat_practical_exam': False,
            'additional_lessons': False
        }),
        (90, 5, {                               # Test case 2 based on business rule 2
            'license_granted': False,
            'repeat_theory_exam': False,
            'repeat_practical_exam': True,
            'additional_lessons': False
        }),
        (50, 1, {                               # Test case 3 based on business rule 3
            'license_granted': False,
            'repeat_theory_exam': True,
            'repeat_practical_exam': False,
            'additional_lessons': False
        }),
        (50, 5, {                               # Test case 4 based on business rule 4
            'license_granted': False,
            'repeat_theory_exam': True,
            'repeat_practical_exam': True,
            'additional_lessons': True
        }),

        #
        # Boundary value-based test cases
        #

        # Theory exam points (a middle value is used for practical exam errors)

        (0, 1, {                               # Valid partition 0-84: lower boundary value
            'license_granted': False,
            'repeat_theory_exam': True,
            'repeat_practical_exam': False,
            'additional_lessons': False
        }),
        (1, 1, {                               
            'license_granted': False,
            'repeat_theory_exam': True,
            'repeat_practical_exam': False,
            'additional_lessons': False
        }),
        (2, 1, {                               
            'license_granted': False,
            'repeat_theory_exam': True,
            'repeat_practical_exam': False,
            'additional_lessons': False
        }),
        (83, 1, {                               
            'license_granted': False,
            'repeat_theory_exam': True,
            'repeat_practical_exam': False,
            'additional_lessons': False
        }),
        (84, 1, {                               # Valid partition 0-84: upper boundary value
            'license_granted': False,
            'repeat_theory_exam': True,
            'repeat_practical_exam': False,
            'additional_lessons': False
        }),
        (85, 1, {                               # Valid partition 85-100: lower boundary value
            'license_granted': True,
            'repeat_theory_exam': False,
            'repeat_practical_exam': False,
            'additional_lessons': False
        }),
        (86, 1, {                               
            'license_granted': True,
            'repeat_theory_exam': False,
            'repeat_practical_exam': False,
            'additional_lessons': False
        }),
        (99, 1, {                               
            'license_granted': True,
            'repeat_theory_exam': False,
            'repeat_practical_exam': False,
            'additional_lessons': False
        }),
        (100, 1, {                              # Valid partition 85-100: upper boundary value           
            'license_granted': True,
            'repeat_theory_exam': False,
            'repeat_practical_exam': False,
            'additional_lessons': False
        }),

        # Practical exam errors (a middle value is used for theory exam points)

        (90, 0, {                              # Partition 0-2: lower boundary value           
            'license_granted': True,
            'repeat_theory_exam': False,
            'repeat_practical_exam': False,
            'additional_lessons': False
        }),
        (90, 1, {                              
            'license_granted': True,
            'repeat_theory_exam': False,
            'repeat_practical_exam': False,
            'additional_lessons': False
        }),
        (90, 2, {                              # Partition 0-2: upper boundary value           
            'license_granted': True,
            'repeat_theory_exam': False,
            'repeat_practical_exam': False,
            'additional_lessons': False
        }),
        (90, 3, {                              # Partition 3-MAX INTEGER: lower boundary value           
            'license_granted': False,
            'repeat_theory_exam': False,
            'repeat_practical_exam': True,
            'additional_lessons': False
        }),
        (90, 4, {                              
            'license_granted': False,
            'repeat_theory_exam': False,
            'repeat_practical_exam': True,
            'additional_lessons': False
        }),
        (90, 5, {                              
            'license_granted': False,
            'repeat_theory_exam': False,
            'repeat_practical_exam': True,
            'additional_lessons': False
        }),
        (90, sys.maxsize, {                     # Edge case: maximum integer in Python                  
            'license_granted': False,
            'repeat_theory_exam': False,
            'repeat_practical_exam': True,
            'additional_lessons': False
        }),
        (90, sys.maxsize + 1, {                 # Edge case: maximum integer in Python (it is converted to long)
            'license_granted': False,
            'repeat_theory_exam': False,
            'repeat_practical_exam': True,
            'additional_lessons': False
        }),

    ])
    def test_drivers_license_passes(self, theory_exam_points, practical_exam_errors, output):
        assert drivers_license_exam_evaluation(theory_exam_points, practical_exam_errors) == output

    #
    # Negative testing
    #    

    # Theory exam points
    @pytest.mark.parametrize('theory_exam_points, practical_exam_errors', [
        
        # Equivalence partition-based test cases

        (120, 1),                   # middle value for the invalid partition 101-MAX INTEGER

        # Boundary value-based test case

        (101, 1),                   # lower boundary value for the invalid partition 101-MAX INTEGER

        # Edge cases 

        (sys.maxsize, 1),           # Maximum integer in Python
        (sys.maxsize + 1, 1),       # Maximum integer in Python + 1 (it is converted to long)

    ])
    def test_drivers_license_fails(self, theory_exam_points, practical_exam_errors):
        with pytest.raises(ValueError) as error_info:
            drivers_license_exam_evaluation(theory_exam_points, practical_exam_errors)
        assert str(error_info.value) == 'There can not be more than 100 points for a theory exam.'

    # Theory exam points
    @pytest.mark.parametrize('theory_exam_points, practical_exam_errors', [
        
        # Equivalence partition-based test case

        (-50, 1),                   # middle value for the invalid partition MIN INTEGER- -1

        # Boundary values-based test cases

        (-2, 1),                    
        (-1, 1),                    # upper boundary value for the invalid partition MIN INTEGER- -1

        # Edge cases 

        (-sys.maxsize, 1),           # Minimum integer in Python
        (-sys.maxsize - 1, 1),       # Minimum integer in Python - 1 (it is converted to long)

    ])
    def test_drivers_license_fails(self, theory_exam_points, practical_exam_errors):
        with pytest.raises(ValueError) as error_info:
            drivers_license_exam_evaluation(theory_exam_points, practical_exam_errors)
        assert str(error_info.value) == 'The number of exam points cannot be negative.'

    # Practical exam errors
    @pytest.mark.parametrize('theory_exam_points, practical_exam_errors', [
        
        # Equivalence partition-based test case

        (90, -5),                   # middle value for the invalid partition MIN INTEGER- -1

        # Boundary value-based test case

        (90, -1),                   # upper boundary value for the invalid partition MIN INTEGER- -1

        # Edge cases 

        (90, -sys.maxsize),         # Minimum integer in Python
        (90, -sys.maxsize - 1),     # Minimum integer in Python - 1 (it is converted to long)

    ])
    def test_drivers_license_fails(self, theory_exam_points, practical_exam_errors):
        with pytest.raises(ValueError) as error_info:
            drivers_license_exam_evaluation(theory_exam_points, practical_exam_errors)
        assert str(error_info.value) == 'The number of practical exam errors cannot be negative.'

    # Other edge cases
    
    @pytest.mark.parametrize('theory_exam_points, practical_exam_errors', [
        ('Hello', 1),
        (90, 'Hello')
    ])
    def test_drivers_license_wrong_data_type_fails(self, theory_exam_points, practical_exam_errors):
        with pytest.raises(ValueError) as error_info:
            drivers_license_exam_evaluation(theory_exam_points, practical_exam_errors)
        assert str(error_info.value)[0:40] == 'invalid literal for int() with base 10: '        