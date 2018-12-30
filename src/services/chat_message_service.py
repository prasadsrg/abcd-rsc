from db import session
from utils.util import uid, model_to_dict
from models.chat_message_model import ChatMessageModel
from models.chat_room_model import ChatRoomModel
from mappers.chat_room_mapper import ChatRoomMapper
from mappers.chat_message_mapper import ChatMessageMapper
import datetime


class ChatMessageService:

    session_info = None

    def mapping(self, model, view):
        print("=======================================================================")
        print(view)
        print("=======================================================================")
        if model.id is None:
            model.id = uid()
            model.room = ChatRoomModel()
            # model.room.id = uid()
            model.roomId = view["roomId"]
            # model.room.name = view["name"] if view["isIndividual"] is True else uid()
            # model.room.isIndividual = view["isIndividual"]
            model.profileId = view["profileId"]
            model.message = view["message"]
        model.updatedBy = "SYSTEM"
        model.updatedOn = datetime.datetime.now()
        # ChatRoomMapper(model, view.get("room")).model_mapping()
        ChatMessageMapper(model, view).model_mapping()

    def is_validate(self, model, is_new):

        query = session.query(ChatMessageModel)\
            .filter((ChatMessageModel.messageId == model.messageId) | (ChatMessageModel.roomId == model.roomId))
        data_list = query.all()
        if data_list:
            if is_new:
                return False
            else:
                for item in data_list:
                    if item.id != model.id:
                        return False
        return True

    def save(self, req_data):
        chat_message = None
        _id = req_data.get('id', None)
        if _id is not None:
            chat_message = session.query(ChatMessageModel).filter_by(id=_id).first()
        if chat_message is None:
            chat_message = ChatMessageModel()
        self.mapping(chat_message, req_data)
        # if self.is_validate(chat_message, False if _id else True):
        session.add(chat_message)
        session.commit()
        return {'message': 'Saved Successfully', 'id': chat_message.id}
        # else:
        #     raise Exception('Record already exists')

    def model(self, _id):
        return session.query(ChatMessageModel).filter_by(id=_id).first()

    def search(self, req_data):
        query = session.query(ChatMessageModel)
        if req_data and req_data.get('roomId') is not None:
            query = query.filter(ChatMessageModel.roomId == (req_data["roomId"]))
        data_list = query.limit(9999).all()
        data_list = list(map(model_to_dict, data_list))
        return data_list

    @staticmethod
    def map_maessage_model(data):
        data = model_to_dict(data)
        del data["profile"]