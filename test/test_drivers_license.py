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

    @pytest.mark.parametrize('theory_exam_points, practical_exam_errors', [
        
        # Equivalence partition-based test case

        (120, 1),                   # Theory exam points: middle value for the invalid partition

        # Boundary value-based test case

        (101, 1),                   # Theory exam points: lower boundary value for the invalid partition

        # Edge cases 

        (sys.maxsize, 1),           # Maximum integer in Python
        (sys.maxsize + 1, 1),       # Maximum integer in Python + 1 (it is converted to long)

    ])
    def test_drivers_license_fails(self, theory_exam_points, practical_exam_errors):
        with pytest.raises(ValueError) as error_info:
            drivers_license_exam_evaluation(theory_exam_points, practical_exam_errors)
        assert str(error_info.value) == 'There can not be more than 100 points for a theory exam.'

    # Other edge cases
    
    def test_drivers_license_negative_theory_exam_points_fails(self):
        with pytest.raises(ValueError) as error_info:
            drivers_license_exam_evaluation(-1, 1)
        assert str(error_info.value) == 'The number of exam points cannot be negative.'
    
    def test_drivers_license_negative_practical_exam_errors_fails(self):
        with pytest.raises(ValueError) as error_info:
            drivers_license_exam_evaluation(90, -1)
        assert str(error_info.value) == 'The number of practical exam errors cannot be negative.'

    @pytest.mark.parametrize('theory_exam_points, practical_exam_errors', [
        ('Hello', 1),
        (90, 'Hello')
    ])
    def test_drivers_license_wrong_data_type_fails(self, theory_exam_points, practical_exam_errors):
        with pytest.raises(ValueError) as error_info:
            drivers_license_exam_evaluation(theory_exam_points, practical_exam_errors)
        assert str(error_info.value)[0:40] == 'invalid literal for int() with base 10: '        