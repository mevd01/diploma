class Room:
    def __init__(self,ID, rooms_amount):
        self.ID = ID
        self.rooms_amount=rooms_amount
        self.rooms_comfort = 0
        self.room_inside=[0]*rooms_amount
