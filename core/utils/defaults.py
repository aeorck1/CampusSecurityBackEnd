"""The module define default values or constants"""
import re

DEFAULT_COUNTRY = 'Nigeria'


class FileSizeLimit:
    PROFILE_IMAGE_SIZE_LIMIT = 800  # 800 KB


class Regex:

    NG_PHONE_NUMBER_REGEX = re.compile("(?:\\+234|0)\\d{10}")

    GLOBAL_PHONE_NUMBER_REGEX = re.compile("\\+\\d{3}\\d+")
