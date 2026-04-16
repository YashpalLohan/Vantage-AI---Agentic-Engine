import os
from tavily import TavilyClient
from dotenv import load_dotenv
load_dotenv()
t = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))
q = '"software developer intern" hiring in "Remote" (site:jobs.lever.co OR site:boards.greenhouse.io OR site:myworkdayjobs.com OR site:jobs.ashbyhq.com OR site:careers.smartrecruiters.com OR site:apply.workable.com) -site:linkedin.com -site:naukri.com -site:internshala.com -site:indeed.com -site:glassdoor.com -site:wellfound.com'
res = t.search(query=q, max_results=15)
print(len(res.get('results', [])))
