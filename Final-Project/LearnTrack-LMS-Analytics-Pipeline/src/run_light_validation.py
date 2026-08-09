import csv
from collections import Counter, defaultdict
import os

RAW_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'raw')
if not os.path.exists(RAW_DIR):
    RAW_DIR = os.path.join(os.getcwd(), 'data', 'raw')

paths = {
    'learners': os.path.join(RAW_DIR, 'learners.csv'),
    'courses': os.path.join(RAW_DIR, 'courses.csv'),
    'enrolment_activity': os.path.join(RAW_DIR, 'enrolment_activity.csv')
}

report = []

# learners
with open(paths['learners'], encoding='utf-8') as f:
    reader = csv.DictReader(f)
    learners = list(reader)
report.append(f"learners: rows={len(learners)} header_columns={len(learners[0].keys()) if learners else 0}")

# courses
with open(paths['courses'], encoding='utf-8') as f:
    reader = csv.DictReader(f)
    courses = list(reader)
blank_instructor = sum(1 for r in courses if (r.get('instructor_name') is None) or (r.get('instructor_name').strip()==''))
report.append(f"courses: rows={len(courses)} blank_instructor_name={blank_instructor}")

# enrolment_activity
with open(paths['enrolment_activity'], encoding='utf-8') as f:
    reader = csv.DictReader(f)
    enrol = list(reader)
report.append(f"enrolment_activity: rows={len(enrol)}")

# duplicate enrolment_id
enrol_ids = [r['enrolment_id'] for r in enrol]
dups = [eid for eid,count in Counter(enrol_ids).items() if count>1]
report.append(f"duplicate_enrolment_id_count={len(dups)} duplicated_ids_sample={dups[:10]}")

# blank last_activity_date
blank_last = sum(1 for r in enrol if (r.get('last_activity_date') is None) or (r.get('last_activity_date').strip()==''))
report.append(f"blank_last_activity_date_count={blank_last} ({blank_last/len(enrol):.2%})")

# assessment_score blank vs non-blank by status
assessment_blank = sum(1 for r in enrol if (r.get('assessment_score') is None) or (r.get('assessment_score').strip()==''))
report.append(f"assessment_score_blank_count={assessment_blank} ({assessment_blank/len(enrol):.2%})")

# actual_completion_date null for non-completed
actual_null_noncompleted=0
for r in enrol:
    status = r.get('status','').strip()
    ac = r.get('actual_completion_date')
    if status!='Completed' and (ac is None or ac.strip()==''):
        actual_null_noncompleted += 1
report.append(f"actual_completion_date_null_for_non_completed={actual_null_noncompleted}")

# sample value checks
sample_enrolments = enrol[:5]
report.append("sample_enrolments_head:")
for s in sample_enrolments:
    report.append(str(s))

# write report
outp = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs', 'validation_report.md')
with open(outp, 'w', encoding='utf-8') as f:
    f.write('# Light Validation Report\n\n')
    f.write('\n'.join(report))

print('\n'.join(report))
print('\nReport written to', outp)
