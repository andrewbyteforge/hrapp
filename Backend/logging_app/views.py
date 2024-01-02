from django.shortcuts import render

import logging
logger = logging.getLogger('logging_app')

def log_message(request):
    logger.debug('This is a debug message')
    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')

# Displays error page
def error_page(request, context=None):    
    return render(request, 'error_page.html', context)
