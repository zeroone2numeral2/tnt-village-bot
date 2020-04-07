import logging
import logging.config
import json
from html import escape

logger = logging.getLogger(__name__)


def html_escape(string, quote=True):
    return escape(string, quote=quote)


def human_readable_size(size, precision=2):
    suffixes = ['b', 'kb', 'mb', 'gb', 'tb']
    suffix_index = 0
    while size > 1024 and suffix_index < 4:
        suffix_index += 1  # increment the index of the suffix
        size = size / 1024.0  # apply the division

    return '%.*f %s' % (precision, size, suffixes[suffix_index])


def human_readable_to_bytes(size: [str, int, float], unit: str):
    unit = unit.strip().lower()
    size = float(size)

    valid_units = ('b', 'kb', 'mb', 'gb', 'tb')
    if unit not in valid_units:
        raise ValueError('invalid measurament unit passed: {}'.format(unit))

    if unit == 'b':
        return int(size)

    i = valid_units.index(unit)
    for _ in range(i):
        size *= 1024

    return round(size)


def load_logging_config(file_name='logging.json'):
    with open(file_name, 'r') as f:
        logging_config = json.load(f)

    logging.config.dictConfig(logging_config)
