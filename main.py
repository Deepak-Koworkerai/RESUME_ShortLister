import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Agent, Task, Crew, Process
from textwrap import dedent
from readResumes import read_resumes


# read the available resumes! from the Resumes Relative Directory
resumes_directory = "Resumes/"
resumes = read_resumes(resumes_directory)


requirements = input('the are the requirements for the role: ?')

# Load variables from the .env file into the environment
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")


llm = ChatGoogleGenerativeAI(model="gemini-pro",
                             verbose=True,
                             temperature=0.5,
                             google_api_key= '' # set up the api key
)

class Agents():
    def resume_filter_agent(self):
		    return Agent(
			role='Senior Resume Analyst',
			goal='Filter out non-essential resume looking into the provided job description',
			backstory=dedent("""\
				As a Senior Resume Analyst, You excel in filtering and analyzing resumes to identify top candidates for
        various positions. With extensive experience in screening and shortlisting resumes,
        you possess a keen eye for detail and a knack for discerning key qualifications and attributes from the provided resume
        """),
      llm=llm,
			verbose=True,
			allow_delegation=False,
      max_iter=5
		)

class Tasks():
    def filter_resumes_task(self, agent, requirements, resume, short_listed):
        return Task(
            description=f"""\
                Analyze a resume and determine if it meets the specified job requirements.

                As a resume screening specialist, your role is crucial in identifying top candidates 
                for further evaluation. Your expertise in resume analysis will be instrumental in selecting 
                candidates who closely match the job requirements. Pay close attention to key qualifications, 
                relevant experience, and essential skills outlined in the job description.

                requirements : {requirements}

                RESUMES
                -----------------
                      {resume}
               Criteria for Evaluation:
                Ensure that the resume meets the minimum criteria for the position. 
                Focus on selecting candidates whose qualifications align closely with the job requirements.

                Outcome:
                If the resume is deemed eligible, 
                the candidate's name, email, phone number, and LinkedIn profile to the {short_listed} list. 
                Note : if not eligible return 'null'
            """,
            expected_output="""List of shortlisted candidates""",
            context=[],
            input_data=(requirements, resume, short_listed),
            agent=agent
        )

from crewai import Crew, Process

agents = Agents()
tasks = Tasks()

agent = agents.resume_filter_agent()

short_listed_candidates = []

for resume_dict in resumes:
    filename, resume_text = list(resume_dict.items())[0]  # Get filename and text
    task = tasks.filter_resumes_task(agent, requirements, resume_text, short_listed_candidates)
    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True,
        process=Process.sequential,
        full_output=True,
        share_crew=False,
    )
    result = crew.kickoff()
    out = result['final_output']
    if out !={} or out!='null':
    
  #  Update shortlisted candidates with the output data from the crew execution
      short_listed_candidates.append(out)


print("Shortlisted Candidates:")
for candidate in short_listed_candidates:
    print(candidate)
