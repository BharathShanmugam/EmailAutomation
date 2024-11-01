import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from email import encoders
from email.mime.base import MIMEBase
import os
import smtplib
import logging
from datetime import datetime
LOG_PATH = f"/home/bharath/Documents/MYEMAIL/STORE/LOGS/{datetime.now().strftime('%Y-%m-%d')}"
os.makedirs(LOG_PATH, exist_ok=True)
email_logger = logging.getLogger('email')
email_log_file = os.path.join(LOG_PATH, "email.log")
email_handler = logging.FileHandler(email_log_file)
email_logger.addHandler(email_handler)
email_logger.setLevel(logging.INFO)
from dotenv import load_dotenv


def reload_dotenv():
    
    for key, value in os.environ.items():
        if key.startswith(""):  
            del os.environ[key]

   
    load_dotenv()

load_dotenv()
reload_dotenv()

EMAILID=os.getenv("EMAILID")
EMAILPASSWORD=os.getenv("EMAILPASSWORD")


def send_email(firstname: str, email: str, subject: str, company: str, role: Optional[str] = None):
    try:
        if not firstname:
            firstname = "Hiring Manager"
        if not company:
            company = "your Company"

     
        # body = f"""
        # <html>
        # <body style="font-family: Arial, sans-serif; line-height: 1.5; color: #333;">
        #     <p>Dear {firstname},</p>

        #     <p>I am reaching out to express my interest in any current or future openings at 
        #      {f'<strong>{company}</strong>' if company != "your company" else company} that align with my skills in backend development and cloud technologies. 
        #     With hands-on experience in both areas, I am eager to contribute my technical abilities and collaborate 
        #     with your team to build innovative, efficient solutions.</p>

        #     <p>After earning my B.Tech in Electronics and Communication Engineering, I joined TekStructer as a 
        #     Backend Engineer intern, where I gained eight months of experience optimizing backend systems and 
        #     developing APIs within AWS Cloud environments. My recent projects include a productivity app built 
        #     with FastAPI and Docker, and a CRM solution that integrates third-party services like WhatsApp and 
        #     Razorpay. These experiences have not only strengthened my backend and cloud skills but also 
        #     highlighted the importance of seamless, scalable solutions that enhance user experience.</p>

        #     <p>I am enthusiastic about the possibility of contributing to  {f'<strong>{company}</strong>' if company != "your company" else company} and would 
        #     welcome the opportunity to discuss any roles where my skills in backend and cloud development could 
        #     be of value. I have attached my resume for your reference, and I am looking forward to the chance to 
        #     discuss how my background aligns with your team’s needs.</p>

        #     <p>Thank you for your time and consideration. I look forward to connecting.</p>

        #     <p>Warm regards,<br>
        #     Bharath Shanmugam<br>
        #     Contact: +91 7981346556<br>
        #     <a href="mailto:bharathshanmugam33@gmail.com">bharathshanmugam33@gmail.com</a><br>
        #     <a href="https://www.linkedin.com/in/bharath-s-337191222/" target="_blank">LinkedIn</a> | 
        #     <a href="https://bharathshanmugam.github.io/" target="_blank">Portfolio</a>
        #     </p>
        # </body>
        # </html>
        # """   
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.5; color: #333;">
            <p>Dear {firstname},</p>

            <p>I hope this message finds you well. I am reaching out to express my interest in any current or upcoming opportunities at <strong>{company}</strong> that align with my skills in backend development and cloud technologies. With hands-on experience in both areas, I am eager to contribute my technical expertise and collaborate with your team to build innovative, efficient solutions.</p>

            <p>Since earning my B.Tech in Electronics and Communication Engineering, I have worked as a Backend Engineer intern at TekStructer, gaining eight months of experience in optimizing backend systems and developing APIs within AWS Cloud environments. My recent projects include:</p>
            <ul>
                <li>A productivity application, built using FastAPI and Docker, focused on streamlining task management.</li>
                <li>A CRM solution integrating third-party services like WhatsApp and Razorpay to enhance user engagement and provide seamless payment options.</li>
            </ul>

            <p>These experiences have not only strengthened my technical skills but also underscored the importance of building scalable, user-focused solutions that deliver real value to end-users.</p>

            <p>I am excited about the prospect of contributing to <strong>{company}</strong> and welcome the opportunity to discuss how my skills in backend development and cloud computing could be a valuable asset to your team. For your convenience, I have attached my resume, and I would be delighted to provide any additional information needed.</p>

            <p>Thank you for your time and consideration. I look forward to the opportunity to connect and explore ways I can contribute to your team’s success.</p>

            <p>Warm regards,<br>
            Bharath Shanmugam<br>
            Contact: +91 7981346556<br>
            Email: <a href="mailto:bharathshanmugam413@gmail.com">bharathshanmugam413@gmail.com</a><br>
            <a href="https://www.linkedin.com/in/bharath-s-337191222/" target="_blank">LinkedIn</a> | 
            <a href="https://bharathshanmugam.github.io/" target="_blank">Portfolio</a>
            </p>
        </body>
        </html>
        """

        msg = MIMEMultipart()
        msg['From'] = EMAILID
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        # Attach resume
        attachment_path = "/home/bharath/Documents/MYEMAIL/Resume/BharathShanmugamResume.pdf"
        if os.path.exists(attachment_path):
            with open(attachment_path, "rb") as attachment:
                mime_base = MIMEBase('application', 'octet-stream')
                mime_base.set_payload(attachment.read())
                encoders.encode_base64(mime_base)
                mime_base.add_header('Content-Disposition', f"attachment; filename=BharathShanmugamResume.pdf")
                msg.attach(mime_base)

        # Sending email using Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAILID, EMAILPASSWORD)
        text = msg.as_string()
        server.sendmail(EMAILID, email, text)
        server.quit()

        # Log successful email sending
        email_logger.info(f"Email sent successfully to {email} with subject: {subject}")

        return True

    except Exception as e:
        # Log error in email sending
        email_logger.error(f"Error sending email to {email}: {str(e)}")
        return False






































# import os
# import smtplib
# import logging
# from typing import Optional
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders

# # Configure logging for email sending
# LOG_FOLDER = "/home/bharath/Documents/MYEMAIL/STORE/LOGS"
# CURRENT_DATE = datetime.now().strftime('%Y-%m-%d')
# LOG_PATH = os.path.join(LOG_FOLDER, CURRENT_DATE)
# os.makedirs(LOG_PATH, exist_ok=True)

# email_log_file = os.path.join(LOG_PATH, "email.log")
# email_logger = logging.getLogger('email')
# email_logger.setLevel(logging.INFO)
# email_handler = logging.FileHandler(email_log_file)
# email_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# email_handler.setFormatter(email_formatter)
# email_logger.addHandler(email_handler)

# EMAILID = os.getenv("EMAILID")
# EMAILPASSWORD = os.getenv("EMAILPASSWORD")

# def send_email(firstname: Optional[str], email: str, subject: str, company: Optional[str], role: Optional[str] = None) -> bool:
#     """Send an email with optional role and logging."""
#     try:
#         # Create the email body in HTML format
#         body = f"""
#         <html>
#         <body>
#         <p>Dear {firstname if firstname else ''},</p>

#         <p>I hope this email finds you well. I came across your contact information on LinkedIn and wanted to reach out 
#         to inquire about any current or upcoming opportunities at <strong>{company if company else 'your company'}</strong> that align with my background 
#         in backend development and cloud technologies.</p>

#         <p>I have 7 months of internship experience as a Backend Engineer, where I focused on backend development using Python 
#         and cloud infrastructure on AWS. My technical expertise includes:</p>
#         <ul>
#             <li>Backend Development: Python</li>
#             <li>API Frameworks: FastAPI, GraphQL, Apache Kafka</li>
#             <li>Databases: MySQL, SQL, PostgreSQL</li>
#             <li>Cloud Platforms: AWS (VPC, EC2, S3, RDS, Lambda, SNS)</li>
#             <li>Containerization: Docker</li>
#             <li>Operating Systems: Windows, Linux</li>
#             <li>Tools: Git, GitHub, VSCode</li>
#         </ul>

#         <p>In my previous projects, I have successfully contributed to CRM systems and productivity applications, 
#         enhancing my skills in creating robust, scalable backend solutions on the AWS cloud.</p>

#         <p>I have attached my resume for your review, and I would greatly appreciate the opportunity to discuss how 
#         my experience and knowledge can contribute to your team.</p>

#         <p>Thank you for considering my inquiry, and I look forward to the possibility of connecting.</p>

#         <p>Best regards,<br>
#         Bharath<br>
#         Contact: +917981346556<br>
#         <a href="https://www.linkedin.com/in/bharath/" title="https://www.linkedin.com/in/bharath/" target="_blank">LinkedIn</a><br>
#         <a href="https://bharathshanmugam/" title="https://bharathshanmugam/" target="_blank">Personal Website</a>
#         </p>
#         </body>
#         </html>
#         """

#         msg = MIMEMultipart()
#         msg['From'] = EMAILID
#         msg['To'] = email
#         msg['Subject'] = subject
#         msg.attach(MIMEText(body, 'html'))  # Attach HTML body

#         # Attach resume
#         attachment_path = "/home/bharath/Documents/MYEMAIL/Resume/BharathShanmugamResume.pdf"
#         if os.path.exists(attachment_path):
#             with open(attachment_path, "rb") as attachment:
#                 mime_base = MIMEBase('application', 'octet-stream')
#                 mime_base.set_payload(attachment.read())
#                 encoders.encode_base64(mime_base)
#                 mime_base.add_header('Content-Disposition', f"attachment; filename=BharathShanmugamResume.pdf")
#                 msg.attach(mime_base)

#         # Sending email using Gmail's SMTP server
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(EMAILID, EMAILPASSWORD)
#         text = msg.as_string()
#         server.sendmail(EMAILID, email, text)
#         server.quit()

#         # Log successful email sending
#         email_logger.info(f"Email sent successfully to {email} with subject: {subject}")

#         return True

#     except Exception as e:
#         # Log error in email sending
#         email_logger.error(f"Error sending email to {email}: {str(e)}")
#         return False
