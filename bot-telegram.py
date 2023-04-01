#Author: Arman Idrisi

import telebot
import openai


#Bot Api Token
API_TOKEN = '6291839486:AAFg0hQdeTOi-zQe_7TOIvIkNQJ82vc-Duc'

#Openai Api Key
openai.api_key=""


bot = telebot.TeleBot(API_TOKEN)

#Tạo phản hồi
def get_response(msg):
    try:
        completion = openai.Completion.create(
            engine="text-davinci-003",
            prompt=msg,
            max_tokens=2048,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return completion.choices[0].text
    except openai.error.OpenAIError as e:
        return "⚠️Đã xảy ra lỗi khi xử lý câu hỏi của bạn.\nVui lòng thử lại sau......!\nHãy liên hệ cho Nguyễn Ngọc Bảo Châu để có thể xử lý sự cố sớm nhất!"

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
	 # bot.send_message(message.chat.id,message.text)
	   bot.send_message(message.chat.id, """\
Xin chào, Tôi là người máy do anh Nguyễn Ngọc Bảo Châu huấn luyện.

Tôi ở đây để đưa ra câu trả lời cho câu hỏi của bạn.

I Am Created Using Chatgpt Api ! 

Sử dụng /bat_dau_tro_chuyen để bắt đầu đặt câu hỏi.\
""")

# Danh sách username được phép sử dụng các lệnh
allowed_users = ['Chaudvfb']

@bot.message_handler(commands=['view_key'])
def view_key_handler(message):
        # Kiểm tra username của người dùng
    if message.from_user.username in allowed_users:
        # Kiểm tra xem key đã được lưu chưa
        if openai.api_key:
            # Gửi tin nhắn chứa key hiện tại
            bot.send_message(message.chat.id, f'Key hiện tại: \n{openai.api_key}')
        else:
            # Nếu chưa có key nào được lưu, gửi tin nhắn thông báo
            bot.send_message(message.chat.id, 'Không có key nào được lưu!')
    else:
        # Người dùng không được phép sử dụng lệnh, gửi tin nhắn thông báo
        bot.send_message(message.chat.id, 'Bạn không được phép sử dụng lệnh này!')

@bot.message_handler(commands=['add_key'])
def add_key_handler(message):
    # Kiểm tra username của người dùng
    if message.from_user.username in allowed_users:
        # Kiểm tra xem có key hiện tại hay không
        if openai.api_key:
            # Nếu đã có key hiện tại, gửi tin nhắn thông báo không thể thêm key mới
            bot.send_message(message.chat.id, 'Không thể thêm key mới vì đã có key hiện tại!\nBạn hãy sử dụng /delete_key để xóa key cũ trước khi thay đổi key mới!')
        else:
            # Nếu chưa có key hiện tại, yêu cầu người dùng nhập key
            bot.send_message(message.chat.id, 'Vui lòng nhập key của bạn:')
            # Đăng ký bộ xử lý cho bước tiếp theo
            bot.register_next_step_handler(message, save_api_key)
    else:
        # Người dùng không được phép sử dụng lệnh, gửi tin nhắn thông báo
        bot.send_message(message.chat.id, 'Bạn không được phép sử dụng lệnh này!')

def save_api_key(message):
    # Lưu key vào biến openai.api_key
    openai.api_key = message.text
    # Gửi tin nhắn xác nhận đã lưu key thành công
    bot.send_message(message.chat.id, 'Key đã được lưu thành công!')

@bot.message_handler(commands=['delete_key'])
def delete_key_handler(message):
    # Kiểm tra username của người dùng
    if message.from_user.username in allowed_users:
        # Kiểm tra xem key đã được lưu chưa
        if openai.api_key:
            # Xóa key hiện tại
            openai.api_key = ""
            # Gửi tin nhắn xác nhận đã xóa key thành công
            bot.send_message(message.chat.id, 'Key đã được xóa thành công!')
        else:
            # Nếu chưa có key nào được lưu, gửi tin nhắn thông báo
            bot.send_message(message.chat.id, 'Không có key nào được lưu!')
    else:
        # Người dùng không được phép sử dụng lệnh, gửi tin nhắn thông báo
        bot.send_message(message.chat.id, 'Bạn không được phép sử dụng lệnh này!')
# Handle The '/bat_dau_tro_chuyen'
@bot.message_handler(commands=['bat_dau_tro_chuyen'])
def first_process(message):
    bot.send_message(message.chat.id,"Gửi cho tôi câu hỏi của bạn.")
    bot.register_next_step_handler(message,second_process)

def again_send(message):
    bot.register_next_step_handler(message,second_process)

def end_qa_process(message):
    bot.send_message(message.chat.id, "Quá trình hỏi đáp đã kết thúc.\nBạn phải sử dụng /bat_dau_tro_chuyen để bắt đầu một cuộc trò chuyện mới.")
# Thực hiện mọi thao tác dọn dẹp hoặc ghi nhật ký cần thiết tại đây

def second_process(message):
    # Kiểm tra xem tin nhắn có phải là lệnh không
    if message.text.startswith('/'):
        # Xử lý lệnh
        command = message.text.split()[0]
        if command == '/ket_thuc_tro_chuyen':
            end_qa_process(message)
            return
        # elif command == '/help' or command == '/start':
        elif command == '/help':
            # Gửi tin nhắn với nội dung giới thiệu và hướng dẫn sử dụng bot
            bot.send_message(message.chat.id, """\
Đây là trợ giúp!

Sử dụng /ket_thuc_tro_chuyen để kết thúc phiên trò chuyện này.
---Đang cập nhật thêm chức năng mới---\
""")
            again_send(message)
            return
        else:
            bot.send_message(message.chat.id, 'Lệnh không hợp lệ!\nVui lòng sử dụng /help để biết thêm chức năng của bot')
            again_send(message)
            return

# Tạo câu trả lời cho câu hỏi
    response = get_response(message.text)

# Gửi phản hồi cho người dùng
    bot.send_message(message.chat.id, response)

# Đăng ký trình xử lý bước tiếp theo
    again_send(message)

chat_states = {}
bot.infinity_polling()