import logging

logging.basicConfig(level = logging.DEBUG, filename='/home/trenza/Documents/arogga/logt.log', filemode='w', format="{asctime} {levelname:<8} {message}", style='{',)

logging.debug('debug')
logging.info('info')
# logger = logging.getLogger('ftpuploader')
# hdlr = logging.FileHandler('logt.log')
# formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# hdlr.setFormatter(formatter)
# logger.addHandler(hdlr)
# logger.setLevel(logging.INFO)
# logger.info('Cron File is already Running running')
