class user:

    def __init__(self,id):
        self.__mode = 'spending'
        self.__user_id = id
    
    def set_mode(self,mode):
        self.__mode = mode

    def get_mode(self):
        return self.__mode

    def get_user_id(self):
        return self.__user_id