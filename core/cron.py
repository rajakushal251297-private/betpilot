from .views import update_user_balance
import logging

# Set up basic configuration for logging
logging.basicConfig(filename='core.log',level=logging.DEBUG,  # Set the logging level
                    format='%(asctime)s - %(levelname)s - %(message)s')


def my_scheduled_job():
    logging.debug("This is a debug message.")
    print('my_scheduled_job')
    update_user_balance()
    
