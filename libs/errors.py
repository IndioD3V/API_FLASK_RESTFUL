class UniqueViolationError:
    msg = {
            "success": False,
            "error": "UniqueViolation",
            "message": "Key duplicated use method PUT"
        }
    code = 400
    
class InternalServerError:
    def __init__(self, e):
        self.e = e
        self.msg = {
                "success": False,
                "error": "InternalServerError",
                "message": self.e
            }
        self.code = 500