from langgraph.graph import StateGraph, END
from .state import JobState
from .job_nodes import extract_resume_info, search_for_jobs, rank_and_match

def create_job_graph():
    # Initialize the graph
    workflow = StateGraph(JobState)

    # Add the nodes
    workflow.add_node("extract", extract_resume_info)
    workflow.add_node("search", search_for_jobs)
    workflow.add_node("rank", rank_and_match)

    # Set the entry point
    workflow.set_entry_point("extract")

    # Connect the nodes
    workflow.add_edge("extract", "search")
    workflow.add_edge("search", "rank")
    workflow.add_edge("rank", END)

    return workflow.compile()

# This is our engine
job_app = create_job_graph()
