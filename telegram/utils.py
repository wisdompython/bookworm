from bot_src.models import *
from users.models import *



def check_if_user_exists(email):

    return CustomUser.objects.filter(email=email).exists()

def register_group_to_model(tg_id, tg_name, owner, chat_type):

    user = CustomUser.objects.get(email=owner)
    if not TelegramGroup.objects.filter(group_name=tg_name, owner=user).exists():

        tg = TelegramGroup.objects.create(group_id=tg_id, group_name=tg_name, owner=user)

        if chat_type == 'group':
            tg.group = True
            tg.save()
        elif chat_type == 'private':
            tg.private = True
            tg.save() 
    elif TelegramGroup.objects.filter(group_name=tg_name, owner=user).exists():
        # check if the group with id exists
        tg = TelegramGroup.objects.get(group_name=tg_name, owner=user)

        if tg.group_id and tg.group_id == tg_id:
            return "This group is already registered to the model"
        
        elif not tg.group_id:
            tg.group_id = tg_id

            if chat_type == 'group':
                tg.group = True
                tg.save()
        elif chat_type == 'private':
            tg.private = True
        
            tg.save() 
        


            return "Group has been added"
    else:
        return "operation Failed"        