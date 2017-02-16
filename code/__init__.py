"""Spiderdonuts Python code module."""

# Imports
import logging

# Spiderdonuts name
SPIDERDONUTS = 'spiderdonuts'

# Create spiderdonuts logger
logger = logging.getLogger(SPIDERDONUTS)

# Create stream handler and set format
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s'))

# Add handler
logger.addHandler(handler)


def verbose(is_verbose=False):
    """Toggle spiderdonuts verbose mode.

    Parameters
    ----------
    is_verbose : Boolean
        Whether or not spiderdonuts should be verbose (default False).
    """
    if (is_verbose):
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARN)
