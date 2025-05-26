from datetime import datetime

def convert_str_to_datetime(date_str):
    # Try with year, month, day first and with "/" and "-" as separators
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        try:
            return datetime.strptime(date_str, '%Y/%m/%d')
        except ValueError:
            try:
                return datetime.strptime(date_str, '%d-%m-%Y')
            except ValueError:
                try:
                    return datetime.strptime(date_str, '%d/%m/%Y')
                except ValueError:
                    try:
                        return datetime.strptime(date_str, '%m-%d-%Y')
                    except ValueError:
                        try:
                            return datetime.strptime(date_str, '%m/%d/%Y')
                        except ValueError:
                            return None

