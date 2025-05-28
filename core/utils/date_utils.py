from datetime import datetime


class DateFormatter:

    @classmethod
    def natural_ordinal(cls, date_object: datetime):
        # Format the date as "%dst %B, %Y"

        day = date_object.day
        i = (day % 10)
        return date_object.strftime(
            f"{day}{'th' if 10 < day < 14 else ['th', 'st', 'nd', 'rd'][i if i < 4 else 0]} %B, %Y")

    @classmethod
    def mm_yyyy(cls, date_object: datetime):
        return date_object.strftime("%B %Y")

    @classmethod
    def mon_yy(cls, date_object: datetime):
        # e.g. JAN'24 -> January 2024
        return date_object.strftime("%b'%y").upper()
