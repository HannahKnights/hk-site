import os

IS_PRODUCTION = True if os.environ.get('IS_PRODUCTION') else False
DEBUG = True if not IS_PRODUCTION else False
