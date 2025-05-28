import datetime
import os


def format_session(session):
    return session.replace('/', '-')


def get_file_extension(filename):
    _, extension = os.path.splitext(filename)
    return extension.lstrip('.') if extension else ''


def rename_file(filename, new_filename):
    extension = get_file_extension(filename)
    if extension:
        return f'{new_filename}.{extension}'
    return new_filename


def rename_file_with_timestamp(filename, timestamp, prefix='', suffix='', separator='_'):
    timestamp_str = timestamp.strftime('%Y-%m-%d_%H-%M-%S-%f')
    new_filename = timestamp_str

    if prefix:
        new_filename = f'{prefix}{separator}{new_filename}'
    if suffix:
        new_filename = f'{new_filename}{separator}{suffix}'

    new_filename = f'{new_filename}{os.path.splitext(filename)[1]}'
    return new_filename


def rename_file_with_current_timestamp(filename, prefix='', suffix='', seperator='_'):
    return rename_file_with_timestamp(filename, datetime.datetime.now(), prefix, suffix, seperator)


def rename_file_with_date_range(filename, start_date, end_date, prefix='', suffix='', separator='_'):
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    new_filename = f'{start_date_str}{separator}to{separator}{end_date_str}'  # 2024-04-05_to_2024-04-05

    if prefix:
        new_filename = f'{prefix}{separator}{new_filename}'
    if suffix:
        new_filename = f'{new_filename}{separator}{suffix}'

    new_filename = f'{new_filename}{os.path.splitext(filename)[1]}'
    return new_filename
