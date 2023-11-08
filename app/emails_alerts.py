import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_alerts(message_content, reciepents):
    # Office 365 email account details
    username = 'dummyuser@fishbonesolutions.co.uk'
    password = 'Saif1997&'
    msg = MIMEMultipart()
    msg['From'] = username
    msg['Subject'] = 'New Stack Request'
    table_html = """
<table style="border-collapse: collapse; width: 100%;">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="border: 1px solid #ddd; padding: 8px;">Key</th>
      <th style="border: 1px solid #ddd; padding: 8px;">Value</th>
    </tr>
  </thead>
  <tbody>
"""

    for key, value in message_content.items():
        table_html += f"""
        <tr>
      <td style="border: 1px solid #ddd; padding: 8px;"><b>{key}</b></td>
      <td style="border: 1px solid #ddd; padding: 8px;">{value}</td>
    </tr>
        """
    table_html += """
    </tbody>
    </table>
    """
# HTML body
    html_body = f"""
<html>
  <body>
    <h2>Hello, New Stack Request</h2>
    <p>Here are stack details:</p>
        {table_html}
  </body>
</html>
"""

# Add the message body
    msg.attach(MIMEText(html_body, 'html'))

# Add the message body
# Create the SMTP connection
    smtp = smtplib.SMTP('smtp.office365.com', 587)
    smtp.starttls()
    smtp.login(username, password)

# Send the message
    for recipient in reciepents:
        smtp.sendmail(username, str(recipient), msg.as_string())
    smtp.quit()
