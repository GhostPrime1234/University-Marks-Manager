from typing import Any, Dict


def get_subject_data(semester, subject_code: str, subject_name: str = "", sync_source: bool = False) -> Dict[str, Any]:
    if semester.name not in semester.data_persistence.data:
        semester.data_persistence.data[semester.name] = {}

    # Use semester.name, not semester
    if subject_code not in semester.data_persistence.data[semester.name]:
        semester.data_persistence.data[semester.name][subject_code] = {
            "Subject Name": subject_name,
            "Assignments": [],
            "Total Mark": 0,
            "Examinations": {"Exam Mark": 0, "Exam Weight": 0},
            "Sync Source": sync_source,
        }

    return semester.data_persistence.data[semester.name][subject_code]
