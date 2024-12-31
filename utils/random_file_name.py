from datetime import datetime
import uuid


def random_file_name(extension):
    return datetime.now().strftime('%Y%m%d%H%M%S') + \
        str(uuid.uuid4())[:20] + "." + extension
