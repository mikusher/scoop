import os
import smtplib
import time
import logging

from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
import email.encoders as Encoders

from etl.controller.database import create_session
from etl.meta.models import EuroStarNumbers, GameDate

from etl.meta.populate import get_last_insert_day
from etl.utils.log_managment import init_logger

init_logger('{}.log'.format(__name__), __name__)
logger = logging.getLogger(__name__)

SEND_GRID_API_FROM_NAME = os.getenv('SEND_GRID_API_FROM_NAME', 'Mikusher')
SEND_GRID_API_FROM_EMAIL = os.getenv('SEND_GRID_API_FROM_EMAIL', 'mikusher@hotmail.com')
SEND_GRID_API_TO_EMAIL = os.getenv('SEND_GRID_API_TO_EMAIL', 'mikusher@gmail.com')
SEND_GRID_SMTP_HOST = os.getenv('SEND_GRID_SMTP_HOST', 'smtp.sendgrid.net')
SEND_GRID_SMTP_PORT = os.getenv('SEND_GRID_SMTP_PORT', 587)
SEND_GRID_API_USER = os.getenv('SEND_GRID_API_USER', 'apikey')
SEND_GRID_API_KEY = os.getenv('SEND_GRID_API_KEY', '')

DIR_REPO = (os.path.abspath(os.path.dirname(__file__))+'/../')

LOGS = [
    os.path.join(DIR_REPO, 'logs', 'populate.log')
]


def send_email(last_day, numbers, stars):
    msg = MIMEMultipart('alternative')
    msg['From'] = formataddr((SEND_GRID_API_FROM_NAME, SEND_GRID_API_FROM_EMAIL))
    mail_to = os.getenv('SEND_GRID_API_TO_EMAIL', 'mikusher@gmail.com')
    msg['date'] = time.strftime('%Y %H:%M:%S %z')
    msg['Subject'] = os.getenv('SEND_EMAIL_SUBJECT', 'Euro Million Result')
    mail_body = "Last numbers: \nDay: {} \nNumbers:{} \nStars:{}\n".format(last_day, numbers, stars)

    for log in LOGS:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(log, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            'attachment; filename={}'.format(os.path.basename(log))
        )
        msg.attach(part)

    msg['To'] = mail_to
    msg.attach(MIMEText(mail_body, 'plain'))
    try:
        server = smtplib.SMTP(host=SEND_GRID_SMTP_HOST, port=SEND_GRID_SMTP_PORT)
        server.ehlo()
        server.login(SEND_GRID_API_USER, SEND_GRID_API_KEY)
        message = msg.as_string()
        server.sendmail(SEND_GRID_API_FROM_EMAIL, mail_to, message)
        server.quit()
        logger.info("Mail sent to {} at {}".format(mail_to, msg['date']))
    except (Exception,) as error:
        logger.error("Error: {}".format(error))


def last_numbers():
    last_day = False
    conn = None
    try:
        session = create_session()
        uuid_day = session.query(GameDate).order_by(GameDate.game_date.desc()).first().id
        # number and stars in db
        euro_n_s = session.query(EuroStarNumbers).filter(EuroStarNumbers.game_date_id == uuid_day).first()
        if euro_n_s:
            last_day = euro_n_s.game_date.game_date.strftime("%d-%m-%Y")
            last_num = euro_n_s.euro_numbers
            last_stars = euro_n_s.star_numbers
            logger.info("Last numbers: {} {} {}".format(last_day, last_num, last_stars))
            send_email(last_day, last_num, last_stars)
            last_day = True
        session.close()
    except (Exception,) as error:
        logger.error(error)
    finally:
        if conn is not None:
            conn.close()
            logger.info('Database connection closed, for get last day in DB.')
    return last_day
