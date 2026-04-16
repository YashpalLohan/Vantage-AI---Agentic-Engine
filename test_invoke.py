from agent.job_graph import job_app
state = {'resume_text': 'Python, SQL, Machine Learning', 'location': 'Remote', 'min_salary': 'Any', 'extract_data': {}, 'jobs': [], 'final_report': {}}
print('Invoking...')
res = job_app.invoke(state)
print('Success!')
print(res['final_report'])
