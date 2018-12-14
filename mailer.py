import smtplib
from email.mime.multipart import MINEMultipart
from email.mime.textext import MIMEText
from email.mime.image import MIMEImage

fromEmail = "email"
fromPassword = "pasword"

toEmail = 'sendto'

def sendEmail(image):
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = ('Security Update')
	msgRoot['From'] = fromEmail
	msgRoot['To'] = toEmail

	msgAlternative = MIMEMultipart('alternative')
	msgRoot.attach(msgAlternative)
	msgText = MIMEText('found object')
	msgAlternative.attach(msgText)

	msgText = MIMEText('<img src="cid:image1">', 'html')
	msgAlternative.attach(msgText)

	msgImage = MIMEImage(image)
	msgImage.add_header('Content-ID', '<image1>')
	msgRoot.attach(msgImage)

	smtp = smtplib.SMTP('smtp.gmail.com', 587) # change port number
	smtp.starttls()
	smtp.login(fromEmail, fromEmailPassword)
	smtp.sendmail(fromEmail, toEmail, msgRoot.as_string())
	smtp.quit()