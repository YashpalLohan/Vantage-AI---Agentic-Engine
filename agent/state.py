from typing import TypedDict, List, Dict, Optional, Any

# This defines the data for our Job Searcher
class JobState(TypedDict):
    resume_text: str
    location: str
    min_salary: Optional[str]
    extract_data: Dict
    jobs: List[Dict]
    final_report: Any
    