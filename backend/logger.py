import logging

# Set up the logger
logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)  # You can adjust this level (DEBUG, INFO, WARNING, etc.)

# Create file handler
file_handler = logging.FileHandler('app.log')  # Log to this file
file_handler.setLevel(logging.INFO)

# Create a formatter and set it for the file handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s\n')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Optionally, add a console handler if you want logs to also be printed to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Logs printed to console will be at least INFO level
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
