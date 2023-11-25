
class Contract_Manager:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Contract_Manager, cls).__new__(cls)
        return cls._instance

    def perform(self):
        print("DEBUG: PERFORMED")
        return True