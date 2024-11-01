import bcrypt

# To hash a password
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# To check a password
def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


if __name__=="__main__":
    hassh=hash_password("Bharath@1230")
    verify=check_password("Bharath@1230",hassh)
    print(hassh)
    print(verify)





























def send_email(firstname: str, email: str, subject: str, company: str, role: Optional[str] = None):
    try:
        if not firstname:
            firstname = "Hiring Manager"
        if not company:
            company = "your Company"

     
        body = f"""
        <html>
        <body>
        <p>Dear {firstname},</p>


        <p>I hope this email finds you well. I came across your contact information on LinkedIn and wanted to reach out 
        to inquire about the possibility of a job referral for the entry-level position in your company. I understand 
        the value of recommendations in the hiring process and believe that my background aligns well with the needs 
        of your team.</p>

        <p>I also wanted to inquire about any current or upcoming opportunities at {f'<strong>{company}</strong>' if company != "your company" else company} that align 
        with my background in backend development and cloud technologies.</p>

        
        <p>I have 7 months of internship experience as a Backend Engineer, where I focused on backend development using Python 
        and cloud infrastructure on AWS. My technical expertise includes:</p>
        <ul>
            <li>Backend Development: Python,C</li>
            <li>Cloud Platforms: AWS (VPC, EC2, S3, RDS, Lambda, SNS)</li>
            <li>API Frameworks: FastAPI, GraphQL, Apache Kafka</li>
            <li>Databases: MySQL, SQL, PostgreSQL</li>
            <li>Containerization: Docker</li>
            <li>Operating Systems: Windows, Linux</li>
            <li>Tools: Git, GitHub, VSCode</li>
        </ul>

        <p>In my previous projects, I have successfully contributed to CRM systems and productivity applications, 
        enhancing my skills in creating robust, scalable backend solutions on the AWS cloud.</p>

        <p>I have attached my resume for your review, and I would greatly appreciate the opportunity to discuss how 
        my experience and knowledge can contribute to your team.</p>

        <p>Thank you for considering my inquiry, and I look forward to the possibility of connecting.</p>

        <p>Best regards,<br>
        Bharath<br>
        </p>
        </body>
        </html>
        """

        msg = MIMEMultipart()
        msg['From'] = EMAILID
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))  # Attach HTML body

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