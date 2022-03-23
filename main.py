import telebot
import hconfig
import cvaribles
from Student import Teacher
from Student import Student
from telebot import types

bot = telebot.TeleBot(hconfig.TOKEN)

t1 = Teacher()


# region COMMANDS
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    student = types.InlineKeyboardButton(text="Student", callback_data='student')
    teacher = types.InlineKeyboardButton(text='Teacher', callback_data='teacher')
    markup.add(student, teacher)

    bot.send_message(message.chat.id, "Choose:", reply_markup=markup)


@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id, message.chat)
    bot.send_message(1001002883, ":)")


@bot.message_handler(commands=['test'])
def info(message):
    t1.group_list = ["6graders", "7graders"]
    s1 = Student(" ", " ", " ")
    s1.name = "Ali"
    s1.grade = "4"
    s1.id = "132432"

    s2 = Student(" ", " ", " ")
    s2.name = "Nigar"
    s2.grade = "5"
    s2.id = "6432432"

    s3 = Student(" ", " ", " ")
    s3.name = "Murad"
    s3.grade = "7"
    s3.id = "324320"

    t1.student_list.append([])
    t1.student_list.append([])

    t1.student_list[0].append(s1)
    t1.student_list[0].append(s2)
    t1.student_list[0].append(s3)


@bot.message_handler(commands=['groupbar'])
def groupbar(message):
    markup = types.InlineKeyboardMarkup()

    add_gr = types.InlineKeyboardButton(text="Add group", callback_data='add')
    delete_gr = types.InlineKeyboardButton(text='Delete group', callback_data='delete')
    show_gr = types.InlineKeyboardButton(text="Show group", callback_data='show')

    markup.add(add_gr, delete_gr, show_gr)

    cvaribles.subject_success = True

    bot.send_message(message.chat.id, "Choose:", reply_markup=markup)


# endregion


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'teacher':
        bot.send_message(call.message.chat.id, "Enter the teacher's password:")
    elif call.data == 'student':
        pass
    elif call.data == "add":
        cvaribles.add_group_activated = True
        bot.send_message(call.message.chat.id, "Enter name of new group:")
    elif call.data == "delete":
        cvaribles.delete_group_activated = True
        bot.send_message(call.message.chat.id, "Enter name of group you want to delete:")
    elif call.data == "show":
        cvaribles.student_group_buttons = True
        markup = types.InlineKeyboardMarkup()
        group_buttons = []
        if len(t1.group_list) <= 0:
            bot.send_message(call.message.chat.id, "You don't have any groups yet")
        else:
            for i in range(len(t1.group_list)):
                group_buttons.append(types.InlineKeyboardButton(text=t1.group_list[i],
                                                                callback_data=t1.group_list[i]))  # Создаем кнопки групп
                markup.add(group_buttons[i])
            bot.send_message(call.message.chat.id, "Your groups:", reply_markup=markup)
    elif call.data == "add_st":
        bot.send_message(call.message.chat.id, "Enter student's name,grade,id \n Example:Camal Imanov,7,987898776")
        cvaribles.add_student_activated = True
    elif call.data == "delete_st":
        avoid()
        bot.send_message(call.message.chat.id, "Enter student's name to delete \n Example:Camal Imanov")
        cvaribles.delete_student_activated = True
    elif call.data == "show_st":
        if len(t1.student_list[cvaribles.group_index]) <= 0:
            bot.send_message(call.message.chat.id, f"You don't have any students in "
                                                   f"group {t1.group_list[cvaribles.group_index]} yet")
        else:
            avoid()
            try:

                lesson_buttons_increase = []
                lesson_buttons_decrease = []

                for i in range(len(t1.student_list[cvaribles.group_index])):
                    print(f"callback_data=increase_{i}")
                    lesson_buttons_increase.append(
                        types.InlineKeyboardButton(text="\u2705", callback_data=f"increase_{i}"))
                    lesson_buttons_decrease.append(
                        types.InlineKeyboardButton(text="\u274C", callback_data=f"decrease_{i}"))
                bot.send_message(call.message.chat.id, f"Group: {t1.group_list[cvaribles.group_index]}")
                for i in range(len(t1.student_list)):
                    for j in range(len(t1.student_list[i])):
                        bot.send_message(call.message.chat.id, f"Name: {t1.student_list[i][j].name}\n"
                                                               f"Grade: {t1.student_list[i][j].grade}\n"
                                                               f"Id: {t1.student_list[i][j].id}\n")

                        markup = types.InlineKeyboardMarkup()
                        markup.add(lesson_buttons_increase[j], lesson_buttons_decrease[j])
                        print(lesson_buttons_increase[j].callback_data, lesson_buttons_decrease[j].callback_data)
                        bot.send_message(call.message.chat.id, f"Lesson: {t1.student_list[i][j].lesson_num}/8",
                                         reply_markup=markup)
                cvaribles.lesson_control_buttons = True

                markuptest = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

                groupbar = types.KeyboardButton("/groupbar", )

                markuptest.add(groupbar)

                bot.send_message(call.message.chat.id, "_________", reply_markup=markuptest)

            except:
                bot.send_message(call.message.chat.id, 'Try again')
    elif cvaribles.student_group_buttons:
        for i in range(len(t1.group_list)):
            if call.data == t1.group_list[i]:
                cvaribles.group_index = i
                markup = types.InlineKeyboardMarkup()

                add_gr = types.InlineKeyboardButton(text="Add student", callback_data='add_st')
                delete_gr = types.InlineKeyboardButton(text='Delete student', callback_data='delete_st')
                show_gr = types.InlineKeyboardButton(text="Show students", callback_data='show_st')

                markup.add(add_gr, delete_gr, show_gr)

                bot.send_message(call.message.chat.id, f"Group: {t1.group_list[cvaribles.group_index]}", reply_markup=markup)
                break
        cvaribles.student_group_buttons = False
    elif cvaribles.lesson_control_buttons:
        for i in range(len(t1.student_list[cvaribles.group_index])):
            if call.data == f"increase_{i}":
                print(f"increase_{i}")
                t1.student_list[cvaribles.group_index][i].lesson_num += 1
                if t1.student_list[cvaribles.group_index][i].lesson_num >= 8:
                    print('Pay time')  # 8 уроков прошло уведомления
                    t1.student_list[cvaribles.group_index][i].lesson_num = 0
                t1.student_list[cvaribles.group_index][i].lesson_total += 1
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=f"Lesson {t1.student_list[cvaribles.group_index][i].lesson_num}/8")  # Исправить эту херню
                print(t1.student_list[cvaribles.group_index][i].name)
                break
            elif call.data == f"decrease_{i}":
                print(f"decrease_{i}")
                cvaribles.crease_index = i
                t1.student_list[cvaribles.group_index][i].lesson_num -= 1
                if t1.student_list[cvaribles.group_index][i].lesson_num <= 0:
                    t1.student_list[cvaribles.group_index][i].lesson_num = 0
                t1.student_list[cvaribles.group_index][i].lesson_total -= 1

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=f"Lesson {t1.student_list[cvaribles.group_index][i].lesson_num}/8")

                break


@bot.message_handler(content_types=['text'])
def check_password(message):
    if message.text == hconfig.t_password:
        bot.send_message(message.chat.id, "Password is correct")
        bot.send_message(message.chat.id, "Enter full name with attribute \"/name\" "
                                          "\nExample: /name Tom Rider")
        cvaribles.password_success = True
    elif message.text.startswith("/name") and cvaribles.password_success:
        if len(message.text) > 10:
            t1.set_name_surname(message.text.replace("/name", ""))
            t1.set_name_surname(message.text.replace("/name ", ""))
            bot.send_message(message.chat.id, f"Your name is {t1.name}")
            cvaribles.name_success = True
            bot.send_message(message.chat.id, "Enter your subjects with attribute \"/subject\" "
                                              "\nExample: /subject Math English Russian")
        else:
            bot.send_message(message.chat.id, "Try again")
            bot.send_message(message.chat.id, "Enter full name with attribute \"/name\" "
                                              "\nExample: /name Tom")

    elif message.text.startswith("/subject") and cvaribles.name_success:
        if len(message.text) > 10:
            txt = message.text.replace("/subject ", "")
            t1.subject_list = txt.split(" ")

            markup = types.InlineKeyboardMarkup()

            add_gr = types.InlineKeyboardButton(text="Add group", callback_data='add')
            delete_gr = types.InlineKeyboardButton(text='Delete group', callback_data='delete')
            show_gr = types.InlineKeyboardButton(text="Show groups", callback_data='show')

            markup.add(add_gr, delete_gr, show_gr)

            cvaribles.subject_success = True

            bot.send_message(message.chat.id, "Choose:", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Try again")
            bot.send_message(message.chat.id, "Enter your subjects with attribute \"/subject\" "
                                              "\nExample: /subject Math English Russian")
    elif cvaribles.add_group_activated:
        t1.group_list.append(message.text)  # Добавляем новую группу
        cvaribles.add_group_activated = False
        t1.student_list.append([])
        bot.send_message(message.chat.id, f"Group \"{message.text}\" was added successfully")

        cvaribles.subject_success = True
        # region GROUPBAR
        markup = types.InlineKeyboardMarkup()

        add_gr = types.InlineKeyboardButton(text="Add group", callback_data='add')
        delete_gr = types.InlineKeyboardButton(text='Delete group', callback_data='delete')
        show_gr = types.InlineKeyboardButton(text="Show group", callback_data='show')

        markup.add(add_gr, delete_gr, show_gr)

        cvaribles.subject_success = True

        bot.send_message(message.chat.id, "Choose:", reply_markup=markup)
        # endregion
    elif cvaribles.delete_group_activated:
        t1.group_list.remove(message.text)  # Удаляем группу
        bot.send_message(message.chat.id, f"Group \"{message.text}\" was deleted successfully")

        cvaribles.delete_group_activated = False
        # region GROUPBAR
        markup = types.InlineKeyboardMarkup()

        add_gr = types.InlineKeyboardButton(text="Add group", callback_data='add')
        delete_gr = types.InlineKeyboardButton(text='Delete group', callback_data='delete')
        show_gr = types.InlineKeyboardButton(text="Show group", callback_data='show')

        markup.add(add_gr, delete_gr, show_gr)

        cvaribles.subject_success = True

        bot.send_message(message.chat.id, "Choose:", reply_markup=markup)
        # endregion
    elif cvaribles.add_student_activated:
        txt = message.text
        if txt.count(',') == 2:
            info_arr = []

            info_arr = txt.split(',')

            s1 = Student(info_arr[0], info_arr[1], info_arr[2])

            t1.student_list[cvaribles.group_index].append(s1)  # Добавляем студента
            bot.send_message(message.chat.id,
                             f'Student "{s1.name}" has been successfully added to group '
                             f'"{t1.group_list[cvaribles.group_index]}"')

            cvaribles.add_student_activated = False
        else:
            bot.send_message(message.chat.id, "Try again")
            bot.send_message(message.chat.id, "Enter student's name,grade,id \n Example: Camal Imanov,7,987898776")
    elif cvaribles.delete_student_activated:
        try:
            for i in range(len(t1.student_list)):
                for j in range(len(t1.student_list[i])):
                    if t1.student_list[i][j].name == message.text:
                        t1.student_list[cvaribles.group_index].pop(j)
                        bot.send_message(message.chat.id, f"{message.text} was successfully removed from "
                                                          f"group {t1.group_list[cvaribles.group_index]}")
                        break
            bot.send_message(message.chat.id, f"No student with name {message.text}")
        except:
            bot.send_message(message.chat.id, f"No student with name {message.text}")


    else:
        markuptest = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

        groupbar = types.KeyboardButton("/groupbar", )

        markuptest.add(groupbar)

        bot.send_message(message.chat.id, "something wrong, use /help", reply_markup=markuptest)


def avoid():  # Аннулировать если не был данн ожидаеммый ввод
    cvaribles.add_group_activated = False
    cvaribles.delete_group_activated = False
    cvaribles.add_student_activated = False
    cvaribles.delete_student_activated = False


bot.polling(none_stop=True)  # loop working
