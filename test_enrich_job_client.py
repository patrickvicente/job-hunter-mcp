import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Adjust the path to your server's main.py if needed
    server_params = StdioServerParameters(command="python", args=["main.py"])
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            # LodgeX Backend Developer job posting
            job_posting = {
                "title": "Backend Developer",
                "description": (
                    "LodgeX is hiring a Full time Backend Developer role in Melbourne, VIC. Apply now to be part of our team.\n\n"
                    "Job summary:\nLooking for candidates available to work:\nMonday: Morning, Afternoon\nTuesday: Morning, Afternoon\nWednesday: Morning, Afternoon\nThursday: Morning, Afternoon\nFriday: Morning, Afternoon\n1 year of relevant work experience required for this role\n\n"
                    "About LodgeX:\nAt LodgeX, we believe innovation begins by challenging the status quo. We reimagine what the future could look like and build the tools to make that vision real - helping shape meaningful change in the property industry.\n\n"
                    "Our flagship platform, Lapp, is a purpose built electronic conveyancing solution designed by property professionals, for property professionals. It simplifies the complex, time consuming process of property settlement by streamlining communication, automating tasks, and delivering real time updates - all in a clean, user friendly interface.\n\n"
                    "What started as a passion project to bridge the gap between legal tech and practical conveyancing has grown into a trusted platform used by lawyers, conveyancers, and lenders across Australia. Our mission is to save time, reduce hassle, and remove friction from every transaction — delivering smarter, faster e-settlements without compromising quality.\n\n"
                    "We're proud of the journey so far - but there's more to build. That's where you come in.\n\n"
                    "About the Role:\nWe are looking for a junior/mid level backend developer to join our growing team at our Melbourne office.\n\n"
                    "You'll:\n• Build and maintain RESTful APIs in Golang.\n• Model and optimise data schemas in Postgres.\n• Integrate backend services with our React frontend.\n• Collaborate on AWS infrastructure design, CI/CD pipelines, testing, and monitoring.\n• Work hand in hand with engineers, our product manager, and the settlements team to deliver quality user experiences.\n\n"
                    "What We're Looking For:\n• 2–4 years of professional backend development experience.\n• Strong knowledge of Postgres (schema design, indexing, migrations).\n• Proficiency in Golang or another statically typed language.\n• Solid grasp of RESTful API design principles.\n• Version control expertise with Git.\n• Experience developing on Linux or WSL environments.\n• Containerisation skills using Docker.\n• Writing and maintaining automated tests (unit and integration) in Go.\n• Designing and maintaining CI/CD pipelines (e.g., GitHub Actions, Jenkins).\n• Implementing structured logging and basic monitoring (CloudWatch).\n• Applying basic security best practices (input validation, secret management).\n\n"
                    "Nice to Have (But Not Essential)\n• Frontend development experience with React and TypeScript or Javascript.\n• Infrastructure as Code using Terraform or AWS CloudFormation.\n• AWS Certified Solutions Architect or AWS Certified Developer, or equivalent cloud certifications.\n• Hands on experience with AWS services (Lambda, API Gateway, RDS, S3).\n• Familiarity with serverless architectures and microservices patterns.\n• Knowledge of GraphQL or gRPC for API design.\n\n"
                    "Ready to apply?\nSubmit your resume and a short cover letter to ***@lodgex.com.au, outlining why you're interested in joining LodgeX. Bonus points for links to a portfolio, GitHub profile, or side projects.\n\n"
                    "We're looking forward to hearing from you!\n"
                ),
                "company": "LodgeX",
                "location": "Melbourne VIC",
                "job_category": "Backend Development",
                "url": "https://jora.com/job/lodgex-backend-developer",
                "context": {}
            }
            result = await session.call_tool("enrich_job", job_posting)
            print("Tool result for LodgeX Backend Developer:", result)

if __name__ == "__main__":
    asyncio.run(main())