import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import logging
from datetime import datetime

filenametime = datetime.now().strftime('%Y-%m-%d_%H.%M.%S_rat.log')
logging.basicConfig(filename=filenametime, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

def main():
	login, password = 'LOGIN', 'PASSWORD' # <------- Enter your login and password from vk.com!
	vk_session = vk_api.VkApi(login, password)
	vk = vk_session.get_api()
	
	try:
		vk_session.auth(token_only=True)
	except vk_api.AuthError as error_msg:
		print(error_msg)
		return

	longpoll = VkLongPoll(vk_session)

	print("Automatic 'rat' kick. Author: vk.com/jp444")
	chatid = int(input("ID of a chat: "))   					   
	peerid = chatid + 2000000000						  	   
	chatname = str(vk.messages.getChat(chat_id=chatid)["title"]) 							 
	logging.info("Monitoring: " + chatname)					  
	print("Monitoring: " + chatname)							   

	for event in longpoll.listen():
		if event.type == VkEventType.MESSAGE_NEW:
			if event.raw[3] == peerid:
				if event.raw[6]['source_act'] == 'chat_kick_user' or event.raw[6]['source_act'] == 'chat_invite_user':
					if event.raw[6]['source_mid'] == event.raw[6]['from']:
						userid = event.raw[6]['from']
						firstname = str(vk.users.get(user_ids=userid, fields="")[0]["first_name"])
						lastname = str(vk.users.get(user_ids=userid, fields="")[0]["last_name"])
						callingout = firstname + " " + lastname + "(" + userid + ") "
						try:
							kickresult = vk.messages.removeChatUser(chat_id=chatid, user_id=userid)
							if kickresult == 1:
								logging.info(callingout + "was determined rat and got kicked.")
								print(callingout + "was determined rat and got kicked.")
							else:
								logging.error(callingout + "was determined rat and didnt got kicked because of an error.")
								print(callingout + "was determined rat and didnt got kicked because of an error.")	
						except:
							logging.error(callingout + "was determined rat and didnt got kicked because of an error.")
							print(callingout + "was determined rat and didnt got kicked because of an error.")




if __name__ == '__main__':
	main()