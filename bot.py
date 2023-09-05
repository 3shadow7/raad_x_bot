
#? add script to convert txt file to json , for update any change in books auto from coggle.it site

#! --------------------------------------------------------

import traceback
import telebot
from telebot import types , util
import json
import time
from threading  import Thread

#! set up json file section
#? import json data from coggle to use it
with open('new_json_nicehash.json', 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

bot = telebot.TeleBot("6669737678:AAEdmFj6ZC4b5F4-HuYp7CrDqouewVPspmU")

#! global section
check = 0
id = 0
mediagroup_user_store = {"db":[],}
text_messages = {
    "welcomeNewMember":
            u" اهلا بك {name} في مجموعتنا لكلية النفط و الغاز و الطاقات المتجدده <emoje>",
    "goodBayMember":
            u"لقد غادر {name} مجموعتنا <emoji>",
    "leave":
            u"اعتذر على المغادرة , لست مصمم لهذه المجموعه \n\nفي حال اردت استعمالي رجاء تواصل مع سيدي {name} للتفاوض معه في هذا ",
    "bot_data":{
            "about":
                    u"حول :\n\nانا رعد ، روبوت صممني سيدي {name} ، وذلك لغرض تنظيم الصور للمواد الدراسية لهذه المجموعه تحت هاشتاق واحد يجمعها .\n\nو هذا حتى يسهل العثور على صور المواد المراد دراستها .\n\n\nطريقة الاستعمال : \n1. عند ارسالك صوره لمادة رياضه1 ، سأرسل لك تلقائيا قائمه بها اسماء المواد كلها .\n2. اختر القسم الذي تحتويه هذه المادة .\n3. اختر اسم الماده ، رياضه1\n\nوعند الحاجه للبحث عن اسئله رياضه1 :\n1. استعمل الامر /search \n2. ستظهر لك قائمه بها كل المواد \n3. اختر اسم الماده المراد البحث عنها\n4. سأرسل لك هاشتاق معين ، اضغط على الهاشتاق  \n\n\nاصدار البوت : {version}",
            "developer":
                    u"@L3shadow7",
            "version":
                    u"1.1",
                },
    
    
     
}


bot.set_my_commands([
    telebot.types.BotCommand("/search", "للبحث عن المادة التي ترغب بدراستها "),
    telebot.types.BotCommand("/about", "لطرح تفاصيل عن البوت و المطور "),
])



#! about bot section
@bot.message_handler(commands=['about'])
def search(message):
    
    sms = bot.send_message(message.chat.id,text_messages["bot_data"]["about"].format( name = text_messages['bot_data']["developer"] , version = text_messages['bot_data']['version'] )   ) 
    
#! search command section
@bot.message_handler(commands=['search'])
def search(message):
    # Send the first keyboard to user
    global mediagroup_user_store , id
    id += 1
    kb = hashtag_page(id)
    sms = bot.send_message(message.chat.id,"اختر المادة التي تبحث عنها"  ,reply_markup=kb,reply_to_message_id=message.message_id ) 
    mediagroup_user_store["db"].append({id:{"bot_chat_id":sms.chat.id,"bot_message_id":sms.message_id,"bot_user_id":sms.from_user.id,"from_chat_id":message.chat.id,"from_message_id":message.message_id,"from_user_id":message.from_user.id}})
    
    x = 30*60
    t = Thread(target=delete_sleep,args=(id,x))
    t.start()
    # time.sleep(30*60)

    

#! filter mediagroup section
# SimpleCustomFilter is for boolean values, such as is_admin=True
class is_mediagroup(telebot.custom_filters.SimpleCustomFilter):
    key='is_mediagroup'
    @staticmethod
    def check(message):
        global check
        if message.media_group_id != None :
            if check != message.media_group_id :
                check = message.media_group_id
                return message.media_group_id != None 
        if message.media_group_id == None:
            return True

#! leave group section
# # to leave any chat , just my only group he is work on it
@bot.my_chat_member_handler()
def leave(message:types.ChatMemberUpdated):
    update = message.new_chat_member
    # if update.status == "member":
    #     bot.send_message(message.chat.id,text_messages["leave"].format(name=text_messages['bot_data']["developer"]))
    #     bot.leave_chat(message.chat.id)
        
#! welcome and goodbay section
@bot.chat_member_handler()
def user_update(message:types.ChatMemberUpdated):
    new = message.new_chat_member
    if new.status == "member":
        bot.send_message(message.chat.id,text_messages["welcomeNewMember"].format(name=new.user.first_name))
    if new.status == "left":
        bot.send_message(message.chat.id,text_messages["goodBayMember"].format(name=new.user.first_name))



#! reply any photo to set hashtag section
@bot.message_handler(regexp="^هاشتاق")
def delete_any_message(message):
    # Send the first keyboard to user
    global mediagroup_user_store , id
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Get chat member information
    chat_member = bot.get_chat_member(chat_id, user_id)

    if chat_member.status == 'administrator' or chat_member.status == 'creator':
        # User is an admin or creator
        if message.reply_to_message:
            if message.reply_to_message.content_type == "photo":    
                
                id += 1
                kb = hashtag_page(id)
                sms = bot.send_message(message.chat.id,"اختر الهاشتاق المناسب لهذه الصور , ليسهل ايجادها مستقبلا"  ,reply_markup=kb,reply_to_message_id=message.reply_to_message.message_id ) 
                mediagroup_user_store["db"].append({id:{"bot_chat_id":sms.chat.id,"bot_message_id":sms.message_id,"bot_user_id":sms.from_user.id,"from_chat_id":message.chat.id,"from_message_id":message.reply_to_message.message_id,"from_user_id":message.from_user.id}})
                x = 60*60
                t = Thread(target=edit_sleep,args=(sms,x))
                t.start()
    
    else:
        # User is a normal member
        if message.reply_to_message:
            if message.reply_to_message.content_type == "photo": 
                id += 1
                sms = bot.send_message(chat_id, 'عذرا , هذه متاحه فقط للمشرفين ..')  # Don't send any message or perform any action
                mediagroup_user_store["db"].append({id:{"bot_chat_id":sms.chat.id,"bot_message_id":sms.message_id,"bot_user_id":sms.from_user.id,"from_chat_id":message.chat.id,"from_message_id":message.message_id,"from_user_id":message.from_user.id}})
                x = 15
                t = Thread(target=delete_sleep,args=(id,x))
                t.start()
    
    
            
#! auto set hashtags section
@bot.message_handler(is_mediagroup=True  , content_types=["photo"])
def send(message):
    global mediagroup_user_store , id
    id += 1
                    
    kb = hashtag_page(id)
    sms = bot.send_message(message.chat.id,"اختر الهاشتاق المناسب لهذه الصور , ليسهل ايجادها مستقبلا" ,reply_markup=kb,reply_to_message_id=message.message_id ) 
    mediagroup_user_store["db"].append({id:{"bot_chat_id":sms.chat.id,"bot_message_id":sms.message_id,"bot_user_id":sms.from_user.id,"from_chat_id":message.chat.id,"from_message_id":message.message_id,"from_user_id":message.from_user.id}})
    x = 60*60
    t = Thread(target=edit_sleep,args=(sms,x))
    t.start()


#? callback section
@bot.callback_query_handler(func=lambda callback:callback.data)
def check_callback(callback):
    global mediagroup_user_store 

    call_button = callback.data.split()
    try:
        id = int(call_button[0])
    except Exception  :
        print(" call error = ",Exception)
        

        pass
    
    index = None
    for i, item in enumerate(mediagroup_user_store["db"]):
        if id in item.keys():
            index = i
            break
    try:
        print(mediagroup_user_store["db"][index][id]["from_user_id"] ,"==", callback.from_user.id)
        if mediagroup_user_store["db"][index][id]["from_user_id"] == callback.from_user.id :

            #? delete hashtag from btn delete
            if call_button[1] == "delete":
                print("delete")
                bot.delete_message( chat_id = callback.message.chat.id , message_id = callback.message.id  )
                del mediagroup_user_store["db"][index]

            #? delete choses page
            if call_button[1] == "exit":
                # print("chat_id =", mediagroup_user_store["db"][index][id]["chat_id"] ,"| message_id =", mediagroup_user_store["db"][index][id]["message_id"] )
                # print("chat_id =", callback.message.chat.id ,"| message_id =", callback.message.id )

                bot.delete_message( chat_id = callback.message.chat.id , message_id = callback.message.id  )
                del mediagroup_user_store["db"][index]

            #? restart choses
            try:
                if call_button[1] == "restart":
                    kb = hashtag_page(id)
                    bot.edit_message_text( chat_id=callback.message.chat.id,message_id=callback.message.id ,text="اختر الهاشتاق المناسب لهذه الصور , ليسهل ايجادها مستقبلا", reply_markup=kb )
            except Exception  :
                print("restart error = ",Exception)
                

            what_call = None
            titles = ["zero","one","two","three","four","five","six","exit","restart","delete"]
            for k in titles:
                if call_button[1] == k:
                    what_call = k

            #? "مواد عامه" choseses
            if (call_button[1] != "delete") and (call_button[1] != "restart") and (call_button[1] != "exit"):
                show_text = json_data[f"{what_call}"]["name"]
                send_text = json_data[f"{what_call}"]["hashtag"]
                
                #----------------------------
                index_of_page = call_button[3] 
                all_items = len(show_text)
                n_fullpage = all_items/15 
                n_fullpage = int(n_fullpage) -1
                n_btns = all_items%15
                
                add_page = 0
                if n_btns != 0:
                    add_page = 1
                #----------------------------
                #? call btn of "مواد عامه"
                lines = [1,16,31,46,61,76,91,106,121,136,151,166,181,196,211,226,241,256,271,286,]
                try:
                    if call_button[2] == "-1": # basic page
                        print("basic page")
                        index_of_page = int(call_button[3])
                        text = pages(show_text,send_text,lines[0],lines[1],what_call)
                        bot.edit_message_text( chat_id=callback.message.chat.id,message_id=callback.message.id ,text=text, reply_markup= add_btn(id,f"{what_call}",index_of_page,lines[0],lines[1]) )
                    
                    
                    elif call_button[2] == "-3":# forward page
                        print("forward page")
                        
                        if (int(index_of_page) < (n_fullpage + add_page)) : # to check if can we froward page or not
                            print("hi 1")
                            index_of_page = int(index_of_page)
                            # print("show_text =",show_text,"send_text = ",send_text,"|||",b,"---",c)
                            
                            if int(index_of_page) == (n_fullpage) : # to check if we are in the last full page or not 
                                print("hi 2")

                                if (n_btns != 0):# if true then add some lines not all lines
                                    print("hi 3")
                                    text = pages(show_text,send_text,lines[index_of_page +1],lines[index_of_page +1 ]+n_btns,what_call)
                                    bot.edit_message_text( chat_id=callback.message.chat.id,message_id=callback.message.id ,text=text, reply_markup= add_btn(id,f"{what_call}",index_of_page+1,lines[index_of_page +1],lines[index_of_page +1 ]+n_btns) )

                            elif int(index_of_page) != (n_fullpage): # to check if we are in the last full page or not 
                                print(int(index_of_page) ,"=|=", n_fullpage)
                                print("hi 4")
                                print("hi 5")
                                text = pages(show_text,send_text,lines[index_of_page +1],lines[index_of_page +2 ],what_call)
                                bot.edit_message_text( chat_id=callback.message.chat.id,message_id=callback.message.id ,text=text, reply_markup= add_btn(id,f"{what_call}",index_of_page+1,lines[index_of_page +1],lines[index_of_page +2 ] ) )

                    
                    elif  call_button[2] == "-2":# back page  
                        print("back page")
                        if (int(index_of_page) > 0) : # to check if can we back page or not
                            print("hi 1")
                            index_of_page = int(index_of_page)
                            print(index_of_page)
                            text = pages(show_text,send_text,lines[index_of_page -1],lines[index_of_page ],what_call)
                            bot.edit_message_text( chat_id=callback.message.chat.id,message_id=callback.message.id ,text=text, reply_markup= add_btn(id,f"{what_call}",index_of_page-1,lines[index_of_page -1],lines[index_of_page ]) )
                
                except :
                    error_message = traceback.format_exc()
                    print("new error : ",error_message)    
                
                try:
                    print("call from n buttons to send hashtag")
                    # print(callback.message.reply_markup.keyboard[0][0])
                    # print(callback.message.reply_markup.keyboard[0][0].text)

                    if call_button[3] == "-1": # then it must be call from n buttons to send hashtag
                        print("hi 1")
                        
                        if (int(call_button[2]) < lines[1]) and (int(call_button[2]) >= lines[0]) :
                            print("hi 2")
                            calls(call_button, callback.message, what_call,lines[0],lines[1])                      
                        
                        elif (int(call_button[2]) < lines[2]) and (int(call_button[2]) >= lines[1]) :
                            calls(call_button, callback.message, what_call,lines[1],lines[2])           
                        
                        elif (int(call_button[2]) < lines[3]) and (int(call_button[2]) >= lines[2]) :
                            calls(call_button, callback.message, what_call,lines[2],lines[3])           

                        elif (int(call_button[2]) < lines[4]) and (int(call_button[2]) >= lines[3]) :
                            calls(call_button, callback.message, what_call,lines[3],lines[4])           
                except :
                    error_message = traceback.format_exc()
                    print("new error : ",error_message)  

    except Exception :
        error_message = traceback.format_exc()
        print("lord error : ",error_message) 
                
        

#! set up pages contant
#? add basic hashtag page
def hashtag_page(id):
    index_of_page = 0
    kb = types.InlineKeyboardMarkup(row_width=6) 
    chose0 = types.InlineKeyboardButton(text="مواد عامه",callback_data=f"{id} zero -1 {index_of_page}")
    chose1 = types.InlineKeyboardButton(text="بتروفيزياء",callback_data=f"{id} one -1 {index_of_page}")
    chose2 = types.InlineKeyboardButton(text="جيوفيزياء",callback_data=f"{id} two -1 {index_of_page}")
    chose3 = types.InlineKeyboardButton(text="مواد و معادن",callback_data=f"{id} three -1 {index_of_page}")
    chose4 = types.InlineKeyboardButton(text="نفطية",callback_data=f"{id} four -1 {index_of_page}")
    chose5 = types.InlineKeyboardButton(text="بيئيه",callback_data=f"{id} five -1 {index_of_page}")
    chose6 = types.InlineKeyboardButton(text="كيميائية",callback_data=f"{id} six -1 {index_of_page}")
    btn1 = types.InlineKeyboardButton(text="الغاء",callback_data=f"{id} exit -1 {index_of_page}")
    return kb.add(chose0).add(chose1,chose2,chose3).add(chose4,chose5,chose6).add(btn1)

#? add btn to page
def add_btn(id,title,index_of_page,from_n,to_n):

    kb = types.InlineKeyboardMarkup(row_width=5)
    btn0 = types.InlineKeyboardButton(text="<",callback_data=f"{id} {title} -2 {index_of_page}")
    btn1 = types.InlineKeyboardButton(text="رجوع",callback_data=f"{id} restart")
    btn2 = types.InlineKeyboardButton(text=">",callback_data=f"{id} {title} -3 {index_of_page}")
    if title == "five":
        return kb.add(btn0,btn1,btn2,)
    else:
        box = { }
        names = []
        for i in range(from_n,to_n) : 
            print("i = ", i)
            chose  = types.InlineKeyboardButton( text=f"{i}",callback_data= f"{id} {title} {i} -1")
            box[f"chose{i}"] = chose
            names.append(f"chose{i}")

        
        print(to_n," =|= ",from_n)
        print(" first |= ",to_n-from_n)
        print(" sec |= ",to_n+from_n)

        if ((to_n - from_n)==(15)):
            return kb.add(box[names[0]],box[names[1]],box[names[2]],box[names[3]],box[names[4]],box[names[5]],box[names[6]],box[names[7]],box[names[8]],box[names[9]],box[names[10]],box[names[11]],box[names[12]],box[names[13]],box[names[14]],).add(btn0,btn1,btn2,)
        elif ((to_n - from_n)==(14)):
            return kb.add(box[names[0]],box[names[1]],box[names[2]],box[names[3]],box[names[4]],box[names[5]],box[names[6]],box[names[7]],box[names[8]],box[names[9]],box[names[10]],box[names[11]],box[names[12]],box[names[13]],).add(btn0,btn1,btn2,)
        elif ((to_n - from_n)==(13)):
            return kb.add(box[names[0]],box[names[1]],box[names[2]],box[names[3]],box[names[4]],box[names[5]],box[names[6]],box[names[7]],box[names[8]],box[names[9]],box[names[10]],box[names[11]],box[names[12]],).add(btn0,btn1,btn2,)
        elif ((to_n - from_n)==(12)):
            return kb.add(box[names[0]],box[names[1]],box[names[2]],box[names[3]],box[names[4]],box[names[5]],box[names[6]],box[names[7]],box[names[8]],box[names[9]],box[names[10]],box[names[11]],).add(btn0,btn1,btn2,)
        elif ((to_n - from_n)==(11)):
            return kb.add(box[names[0]],box[names[1]],box[names[2]],box[names[3]],box[names[4]],box[names[5]],box[names[6]],box[names[7]],box[names[8]],box[names[9]],box[names[10]],).add(btn0,btn1,btn2,)
        elif ((to_n - from_n)==(10)):
            return kb.add(box[names[0]],box[names[1]],box[names[2]],box[names[3]],box[names[4]],box[names[5]],box[names[6]],box[names[7]],box[names[8]],box[names[9]],).add(btn0,btn1,btn2,)
        elif ((to_n - from_n)==(9)):
            return kb.add(box[names[0]],box[names[1]],box[names[2]],box[names[3]],box[names[4]],box[names[5]],box[names[6]],box[names[7]],box[names[8]],).add(btn0,btn1,btn2,)
        elif ((to_n - from_n)==(8)):
            return kb.add(box[names[0]],box[names[1]],box[names[2]],box[names[3]],box[names[4]],box[names[5]],box[names[6]],box[names[7]],).add(btn0,btn1,btn2,)
        elif ((to_n - from_n)==(7)):
            return kb.add(box[names[0]],box[names[1]],box[names[2]],box[names[3]],box[names[4]],box[names[5]],box[names[6]],).add(btn0,btn1,btn2,)
        elif ((to_n - from_n)==(6)):
            return kb.add(box[names[0]],box[names[1]],box[names[2]],box[names[3]],box[names[4]],box[names[5]],).add(btn0,btn1,btn2,)
        elif ((to_n - from_n)==(5)):
            return kb.add(box[names[0]],box[names[1]],box[names[2]],box[names[3]],box[names[4]],).add(btn0,btn1,btn2,)
        elif ((to_n - from_n)==(4)):
            return kb.add(box[names[0]],box[names[1]],box[names[2]],box[names[3]],).add(btn0,btn1,btn2,)
        elif ((to_n - from_n)==(3)):
            return kb.add(box[names[0]],box[names[1]],box[names[2]],).add(btn0,btn1,btn2,)
        elif ((to_n - from_n)==(2)):
            return kb.add(box[names[0]],box[names[1]],).add(btn0,btn1,btn2,)
        elif ((to_n - from_n)==(1)):
            return kb.add(box[names[0]],).add(btn0,btn1,btn2,)
        
        






#? add contant to page
def pages(ar,en,i,k,what_call):
    if what_call == "five":
        text = f"ليست موجودة بعد ...\n\nلمعرفة الاسباب تواصل مع {text_messages['bot_data']['developer']}\n\n"
        return text
    else:
        text = f"كل مواد {json_data['titles'][f'{what_call}']} :\n\n"
        count = 1
        print("hi 4 === ","show_text =",ar,"send_text = ",en,"|||",i,"---",k)

        for a,e in zip(ar,en) :
            if (count >= i) and (count < k ) :
                
                text += f"[{count}] {a} | {e}\n"
                print("a=", i , "b="  , k, "count = ", count,"text = ",text)   
                count +=1
            elif (count < i)  :
                count +=1
            if count == k:
                print(text)
                return text

    

#? handel calls to send hashtag
def calls(call_data,message,what_call,a,b):
    global mediagroup_user_store , id 
    
    id += 1
    print("here 1")
    call_id = int(call_data[0])
    for i in range(a-1,b-1):

        if call_data[1] == what_call and call_data[2] == str(i+1) :
            print("here 2")
            print(message.reply_to_message.text)
            new_index = None
            for k, item in enumerate(mediagroup_user_store["db"]):
                if call_id in item.keys():
                    new_index = k
                    break
            print(message.reply_to_message.text )
            if message.reply_to_message.text != "/search@SHADOW_filter_IMG_Bot" and message.reply_to_message.text != "/search" :
                kb_delete = types.InlineKeyboardMarkup(row_width=3)
                inline_delete = types.InlineKeyboardButton(text="delete",callback_data=f"{id} delete")
                kb_delete.add(inline_delete)
                print("here 3")
                sms = bot.send_message(chat_id= message.chat.id , text = "#" + json_data[f"{what_call}"]["hashtag"][i] , reply_to_message_id = mediagroup_user_store["db"][new_index][call_id]["from_message_id"] , reply_markup=kb_delete)
                print("here 4")
                mediagroup_user_store["db"].append({id:{"bot_chat_id":sms.chat.id,"bot_message_id":sms.message_id,"bot_user_id":sms.from_user.id,"from_chat_id":mediagroup_user_store["db"][new_index][call_id]["from_chat_id"],"from_message_id":mediagroup_user_store["db"][new_index][call_id]["from_message_id"],"from_user_id":mediagroup_user_store["db"][new_index][call_id]["from_user_id"]}})
                print("here 5")
                x = 10


                t = Thread(target=edit_sleep,args=(sms,x))
                t.start()
                print("here 6")
                
            else :
                print("message is = ",message)
                sms = bot.send_message(chat_id= message.chat.id , text = "اضغط على الهاشتاق : \n\n "+"#" + json_data[f"{what_call}"]["hashtag"][i] , reply_to_message_id = mediagroup_user_store["db"][new_index][call_id]["from_message_id"])
                mediagroup_user_store["db"].append({id:{"bot_chat_id":sms.chat.id,"bot_message_id":sms.message_id,"bot_user_id":sms.from_user.id,"from_chat_id":mediagroup_user_store["db"][new_index][call_id]["from_chat_id"],"from_message_id":mediagroup_user_store["db"][new_index][call_id]["from_message_id"],"from_user_id":mediagroup_user_store["db"][new_index][call_id]["from_user_id"]}})
                x = 15
                t = Thread(target=delete_sleep,args=(id,x))
                t.start()
                

#! time sleep section 
#? edit sms
def edit_sleep(sms,x):
    print("Start")
    time.sleep(x)
    bot.edit_message_reply_markup(chat_id = sms.chat.id, message_id = sms.message_id , reply_markup=None)
    print("End")

#? delete sms
def delete_sleep(id,x):
    print("sleep start")
    time.sleep(x)
    index = None
    for i, item in enumerate(mediagroup_user_store["db"]):
        if id in item.keys():
            index = i
            break 
    print(index,id)
    print(mediagroup_user_store["db"])
    print(mediagroup_user_store["db"][index]) 
    print(mediagroup_user_store["db"][index][id]) 
  
    bot.delete_message( chat_id = mediagroup_user_store["db"][index][id]["bot_chat_id"] , message_id = mediagroup_user_store["db"][index][id]["bot_message_id"]  )
    del mediagroup_user_store["db"][index]
    print("sleep end")

#! final section
# Delete the webhook

bot.delete_webhook()
bot.add_custom_filter(is_mediagroup())
bot.infinity_polling()
