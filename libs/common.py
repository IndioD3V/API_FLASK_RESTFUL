from datetime import date
import datetime

def format_type(value, type_value:type):
        try:
            if type_value == datetime.date:
                return value.strftime('%Y-%m-%d')
            return type_value(value)
        except Exception as e:
            return ''
        
def serialize(value):
    if isinstance(value, date):
        return value.strftime('%Y-%m-%d') 
    return value