# Parameters:
# - The number of points from the theoretical exam (integer number from 0 to 100)
# - The number of errors made by the candidate during the practical exam (integer number 0 or greater)
# The candidate must take both exams. 
# A candidate is granted a driver's license if they meet the following two conditions: 
# - They scored at least 85 points on the theoretical test 
# - They made no more than two errors on the practical test
# If a candidate fails one of the exams, they must repeat this exam. 
# In addition, if the candidate fails both exams, they are required to take additional hours of driving lessons.
def drivers_license_exam_evaluation(theory_exam_points, practical_exam_errors):
    theory_exam_points = int(theory_exam_points)
    practical_exam_errors = int(practical_exam_errors)
    if theory_exam_points > 100:
        raise ValueError('There can not be more than 100 points for a theory exam.')
    if theory_exam_points < 0:
        raise ValueError('The number of exam points cannot be negative.')
    if practical_exam_errors < 0:
        raise ValueError('The number of practical exam errors cannot be negative.')

    output = {
        'license_granted': False,
        'repeat_theory_exam': False,
        'repeat_practical_exam': False,
        'additional_lessons': False
    }
    if theory_exam_points < 85:
        output['repeat_theory_exam'] = True
    if practical_exam_errors > 2:
        output['repeat_practical_exam'] = True

    output['license_granted'] = not output['repeat_theory_exam'] and not output['repeat_practical_exam']
    output['additional_lessons'] = output['repeat_theory_exam'] and output['repeat_practical_exam']

    return output