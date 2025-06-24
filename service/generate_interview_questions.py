
from google import genai

from api.service.interview_qgen_prompt import get_interview_generation_prompt
import os
from dotenv import load_dotenv
load_dotenv()


def generate_interview_questions(job_role, user_resume, job_description, interview_difficulty, question_count):
  GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
  client = genai.Client(api_key=GEMINI_API_KEY)

  prompt = get_interview_generation_prompt(job_role, user_resume, job_description, interview_difficulty, question_count)
  response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

  return response.text








if __name__ == "__main__":
  xg = generate_interview_questions(
    job_role="Machine Learning Engineer",
    user_resume="""
      SKILLS
        Technical Skills Python, C++, Java, Dart, SQL.
        ML and AI Tools PyTorch, TensorFlow, Transformers, Sklearn, Pinecone, OpenCV.
        MLOps and Cloud AWS, MLFlow, Docker, Git.
        Frameworks FastAPI, Langchain, Plotly, Flutter, ASP.NET, ReactJS, VueJS.
        PROJECTS
        Music Recognizer App. Recognizes songs from 3-second clips by matching against a large track database. Built
        embedding models to match humming with sonic signatures, optimized DB for real-time querying, and created an
        audio denoiser. Ideal for high-noise environments like concerts.
        Tech Stack: Pinecone, Huggingface, Gradio, Flutter, Transformers.
        Autism Screening & Therapy: Developed a model for early autism detection using 5-10 second behavioral videos.
        Also created an object-drawing game using computer vision and LLM for therapy, offering real-time feedback based
        on the child’s progress.
        Tech Stack: PyTorch, AWS, Digital Ocean, Modal, Huggingface, Gradio, Spring (Java), MongoDB, VueJS.
        Drag-n-Drop Flutter UI Builder. Built a web tool to create Flutter UI without coding. Used R-tree for efficient
        organization of UI components and generated Flutter code instantly for placed objects.
        Tech Stack: SvelteJS, Flutter, PostgreSQL.
        Echoscript - Research paper as Audio-book: Created an app to listen to academic papers with narration for
        figures, tables, etc. Fine-tuned YOLO for table/figure detection and LLAMA for generating context-based narration.
        Tech Stack: YOLO, LLAMA, Text-to-Speech.
        Airplane Game. Built an airplane simulator with a realistic physics engine, detailed collision system, and a leveling
        system for rewards in a city environment.
        Tech Stack: C++, OpenGL.
      """,
    job_description="""
  At Allstate, great things happen when our people work together to protect families and their belongings from life’s uncertainties. And for more than 90 years our innovative drive has kept us a step ahead of our customers’ evolving needs. From advocating for seat belts, air bags and graduated driving laws, to being an industry leader in pricing sophistication, telematics, and, more recently, device and identity protection.

  Job Description

  Join Allstate Technology Solutions, a pioneering force committed to revolutionizing the way our employees, agencies, and customers interact digitally. Our mission is to harness cutting-edge technology, innovative product design, and the power of artificial intelligence with an emphasis on generative AI, to create a world-class customer experience that transcends boundaries.

  We aim to redefine the customer experience, ensuring consistency across all touchpoints and channels while unveiling substantial opportunities for operational efficiency.

  Become a part of our story...

  At Allstate Technology Solutions, you’ll find a collaborative and dynamic team focused on exploring new capabilities and pushing the boundaries of what is possible. The team works in a continuous innovation cycle of ideas, research, testing, analysis, and delivery.

  As a Machine Learning Engineer (MLE), you relish the challenge of solving business problems using the latest techniques and tools to bring models to life that deliver business value. You bring prior knowledge of machine learning and modeling. Quick to learn and adapt, you are eager to learn how to use all the resources at your disposal—software, algorithms, models, and more—to comprehend and effectively handle intricate problems. You are eager to contribute to model development across the entire lifecycle—from cloud services deployment, model tuning, to application deployment.

  As an MLE, you will be part of a team comprised of junior and senior MLEs. You should be comfortable working collaboratively with other engineers to derive business value from complex machine learning projects.

  Bachelor's or Master's degree in Computer Science, Electrical Engineering, Physics, Mathematics, Statistics, or another quantitative major. A Ph.D. is a plus. 
  Experience applying machine learning algorithms and principles. 
  Ability to collaborate effectively with product managers, engineers, and business leaders. 
  0-3 years of professional experience in machine learning and/or data science 
  1-4 year of experience in programming languages like Python, Java, or C++, including academic and internship experience. 
  1-4 years of experience using machine learning frameworks like PyTorch, TensorFlow, or Scikit-learn, including academic and internship experience. 
  Prior experience using deep learning, natural language processing, computer vision, or knowledge representation and reasoning a plus. 
  Prior experience prompting large language models and/or building RAG applications is a plus. 

  Skills

  Algorithms, Artificial Intelligence (AI), Data Science, Machine Learning, Machine Learning Algorithms, Natural Language Processing (NLP)

  Compensation

  Compensation offered for this role is $104,000.00 - 187,625.00 annually and is based on experience and qualifications.

  The candidate(s) offered this position will be required to submit to a background investigation.

  Joining our team isn’t just a job — it’s an opportunity. One that takes your skills and pushes them to the next level. One that encourages you to challenge the status quo. And one where you can impact the future for the greater good.

  You’ll do all this in a flexible environment that embraces connection and belonging. And with the recognition of several inclusivity and diversity awards, we’ve proven that Allstate empowers everyone to lead, drive change and give back where they work and live.

  Good Hands. Greater Together.

  Allstate generally does not sponsor individuals for employment-based visas for this position.

  Effective July 1, 2014, under Indiana House Enrolled Act (HEA) 1242, it is against public policy of the State of Indiana and a discriminatory practice for an employer to discriminate against a prospective employee on the basis of status as a veteran by refusing to employ an applicant on the basis that they are a veteran of the armed forces of the United States, a member of the Indiana National Guard or a member of a reserve component.

  For jobs in San Francisco, please click “here” for information regarding the San Francisco Fair Chance Ordinance.

  For jobs in Los Angeles, please click “here” for information regarding the Los Angeles Fair Chance Initiative for Hiring Ordinance.

  To view the “EEO is the Law” poster click “here”. This poster provides information concerning the laws and procedures for filing complaints of violations of the laws with the Office of Federal Contract Compliance Programs

  To view the FMLA poster, click “here”. This poster summarizing the major provisions of the Family and Medical Leave Act (FMLA) and telling employees how to file a complaint.

  It is the Company’s policy to employ the best qualified individuals available for all jobs. 
  Therefore, any discriminatory action taken on account of an employee’s ancestry, age, color, disability, genetic information, gender, gender identity, gender expression, sexual and reproductive health decision, marital status, medical condition, military or veteran status, national origin, race (include traits historically associated with race, including, but not limited to, hair texture and protective hairstyles), religion (including religious dress), sex, or sexual orientation that adversely affects an employee's terms or conditions of employment is prohibited. 
  This policy applies to all aspects of the employment relationship, including, but not limited to, hiring, training, salary administration, promotion, job assignment, benefits, discipline, and separation of employment.

    """,

    interview_difficulty="medium",
    question_count=5,
  )

  print(xg)