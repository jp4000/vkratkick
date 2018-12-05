# coding: utf-8
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import logging
from datetime import datetime

logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.INFO, filename = datetime.now().strftime('%Y-%m-%d_%H.%M.%S_ratkick.log'))

BANNER = '''										
  _____       _   _  ___      _    
 |  __ \     | | | |/ (_)    | |   
 | |__) |__ _| |_| ' / _  ___| | __
 |  _  // _` | __|  < | |/ __| |/ /
 | | \ \ (_| | |_| . \| | (__|   < 
 |_|  \_\__,_|\__|_|\_\_|\___|_|\_\
                                   
                                       by: github.com/jp4000'''

def main():
    login, password = "LOGIN", "PASSWORD"
    vk_session = vk_api.VkApi(login, password)
    vk = vk_session.get_api()
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    print(BANNER, end='\n\n')
    print("What this script does?: It kicks people who left the chat or returned to it. In order for it to work, you must be an administrator of the chat!")
    chat = int(input("Chat ID, please (Script will crash if str is passed): "))
    peer = chat + 2000000000
    print("Monitoring: " + vk.messages.getChat(chat_id=chat)["title"])
    logging.info("Monitoring: " + vk.messages.getChat(chat_id=chat)["title"])
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.raw[5] == '' and event.raw[3] == peer and event.raw[6]['source_mid'] == event.raw[6]['from'] and event.raw[6]['source_act'] in ('chat_kick_user', 'chat_invite_user'):
            user = event.raw[6]['from']
            username = vk.users.get(user_ids=user, fields="")[0]["first_name"], vk.users.get(user_ids=user, fields="")[0]["last_name"]
            try:
                kick = vk.messages.removeChatUser(user_id=user, chat_id=chat)
                print(" ".join(username), user, "was determined rat and got kicked")
                logging.info(" ".join(username) + " " + user)
            except:
                print(" ".join(username), user, "didnt got kicked.")
                logging.error(" ".join(username) + " " + user)          
if __name__ == '__main__':
	main()

