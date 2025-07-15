from openai import OpenAI
from markdown import markdown
from weasyprint import HTML




def create_prompt(resume_string: str, jd_string: str) -> str:
    return f"""
You are a professional resume optimization expert specializing in tailoring resumes to specific job descriptions. Your goal is to optimize my resume and provide actionable suggestions for improvement to align with the target role.

### Guidelines:
1. **Relevance**:  
   - Prioritize experiences, skills, and achievements **most relevant to the job description**.  
   - Remove or de-emphasize irrelevant details to ensure a **concise** and **targeted** resume.
   - Limit work experience section to 2-3 most relevant roles
   - Limit bullet points under each role to 2-3 most relevant impacts

2. **Action-Driven Results**:  
   - Use **strong action verbs** and **quantifiable results** (e.g., percentages, revenue, efficiency improvements) to highlight impact.  

3. **Keyword Optimization**:  
   - Integrate **keywords** and phrases from the job description naturally to optimize for ATS (Applicant Tracking Systems).  

4. **Additional Suggestions** *(If Gaps Exist)*:  
   - If the resume does not fully align with the job description, suggest:  
     1. **Additional technical or soft skills** that I could add to make my profile stronger.  
     2. **Certifications or courses** I could pursue to bridge the gap.  
     3. **Project ideas or experiences** that would better align with the role.  

5. **Formatting**:  
   - Output the tailored resume in **clean Markdown format**.  
   - Include an **"Additional Suggestions"** section at the end with actionable improvement recommendations.  

---

### Input:
- **My resume**:  
{resume_string}

- **The job description**:  
{jd_string}

---

### Output:  
1. **Tailored Resume**:  
   - A resume in **Markdown format** that emphasizes relevant experience, skills, and achievements.  
   - Incorporates job description **keywords** to optimize for ATS.  
   - Uses strong language and is no longer than **one page**.

2. **Additional Suggestions** *(if applicable)*:  
   - List **skills** that could strengthen alignment with the role.  
   - Recommend **certifications or courses** to pursue.  
   - Suggest **specific projects or experiences** to develop.
"""


def get_resume_response(prompt: str, api_key: str, model_name: str = "gpt-4o-mini", temperature: float = 0.7) -> str:
    # Setup API client
    token = api_key
    endpoint = "https://models.github.ai/inference"
    model_name = "openai/gpt-4o-mini"

    client = OpenAI(
        base_url=endpoint,
        api_key=token,
    )

    # Make API call
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "Expert resume writer"},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature
    )

    # Extract and return response
    return response.choices[0].message.content

def process_resume(resume, jd_string):
    # read resume
    with open(resume, "r", encoding="utf-8") as file:
        resume_string = file.read()

    # create prompt
    prompt = create_prompt(resume_string, jd_string)

    # generate response
    response_string = get_resume_response(prompt, "enter_your_api_key")
    response_list = response_string.split("## Additional Suggestions")
    
    # extract new resume and suggestions for improvement
    new_resume = response_list[0]
    suggestions = "## Additional Suggestions \n\n" +response_list[1]

    return new_resume, new_resume, suggestions

def export_resume(new_resume):
    try:
        # save as PDF
        output_pdf_file = "resumes/resume_new.pdf"
        
        # Convert Markdown to HTML
        html_content = markdown(new_resume)
        
        # Convert HTML to PDF and save
        HTML(string=html_content).write_pdf(output_pdf_file, stylesheets=['resumes/style.css'])

        return f"Successfully exported resume to {output_pdf_file} 🎉"
    except Exception as e:
        return f"Failed to export resume: {str(e)} 💔"