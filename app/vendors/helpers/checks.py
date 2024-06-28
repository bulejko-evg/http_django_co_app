import re
import magic
import string
import datetime
from functools import partial
from django.conf import settings
from collections import defaultdict
from app.vendors import messages as msg
from app.vendors.base.protocol import FileProtocol
from app.vendors.base.check import check_full_match