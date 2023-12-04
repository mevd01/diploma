import sys
from tkinter.scrolledtext import ScrolledText
import pandas as pd
import random
import string
import tkinter as tk
from tkinter import filedialog
import itertools
from Student import Student
from Room import Room
from Free_place import Free_place

rooms = sorted([4, 4, 4, 4, 4, 3, 3, 2, 2], reverse=True)


def agents_from_excel(file_name):
    excel_data = pd.read_excel(file_name)
    data = pd.DataFrame(excel_data,
                        columns=['Имя', 'Возраст', 'Пол', 'Специализация', 'Курс', 'Предпочтение температуры',
                                 'Отношение к чистоте', 'Уровень шума', 'Как часто нужно быть одному', 'Гигиена',
                                 'Отношение к курению', 'Отношение к учебе'])
    attributes = data.values.tolist()
    return attributes


def agents_creation(attributes):
    agents_list = []
    for i in range(len(attributes)):
        agents_list.append(Student(*attributes[i]))
    return agents_list


def rooms_creation(rooms_list):
    new_list = []
    for i in range(len(rooms_list)):
        new_list.append(Room(i + 1, rooms_list[i]))
    return new_list


def temperature_refactor(list):
    for el in list:
        el.temperature = int(el.temperature[:2])
    return list


def cleaning_refactor(list):
    dict = {'Низкое': 1, 'Среднее': 2, 'Высокое': 3}
    for el in list:
        el.cleaning = dict.get(el.cleaning)
        # print(el.cleaning, type(el.cleaning))
    return list


def sound_refactor(list):
    dict = {'Низкий': 1, 'Средний': 2, 'Высокий': 3}
    for el in list:
        el.sound = dict.get(el.sound)
        # print(el.sound, type(el.sound))
    return list


def loneliness_refactor(list):
    dict = {'Очень редко': 1, 'Редко': 2, 'Не принципиально': 3, 'Часто': 4, 'Очень часто': 5}
    for el in list:
        # el.show_all_info()
        # print(el.loneliness, type(el.loneliness))
        el.loneliness = dict.get(el.loneliness)
        # print(el.loneliness, type(el.loneliness))
    return list


def hygiene_refactor(list):
    dict = {'Редкая': 1, 'Нормальная': 2, 'Хорошая': 3}
    for el in list:
        el.hygiene = dict.get(el.hygiene)
        # print(el.hygiene, type(el.hygiene))
    return list


def smoking_refactor(list):
    dict = {'Отрицательное': 1, 'Нейтральное': 2, 'Положительное': 3}
    for el in list:
        el.smoking = dict.get(el.smoking)
        # print(el.smoking, type(el.smoking))
    return list


def studies_refactor(list):
    dict = {'Не серьезно': 1, 'Не очень серьезно': 2, 'Равнодушно': 3, 'Серьезно': 4, 'Очень серьезно': 5}
    for el in list:
        el.studies = dict.get(el.studies)
        # el.show_all_info()
    return list


def refractor(list):
    temperature_refactor(list)
    cleaning_refactor(list)
    sound_refactor(list)
    loneliness_refactor(list)
    hygiene_refactor(list)
    smoking_refactor(list)
    studies_refactor(list)


def sex_pool(agents):
    female_agents = []
    male_agents = []
    for i in range(len(agents)):
        if agents[i].sex == 'М':
            male_agents.append(agents[i])
        elif agents[i].sex == 'Ж':
            female_agents.append(agents[i])
    return male_agents, female_agents


def students_check_in(students, rooms):
    new_students = sorted(students, key=lambda x: x.year, reverse=False)
    for i in range(len(rooms)):
        for j in range(rooms[i].rooms_amount):
            if len(new_students) != 0:
                rooms[i].room_inside[j] = new_students[0]
                new_students.pop(0)
            else:
                pass

    return rooms


def sprint_rooms(rooms):
    for i in range(len(rooms)):
        print('-----------')
        print('Комната:', rooms[i].ID)
        for j in range(rooms[i].rooms_amount):
            if isinstance(rooms[i].room_inside[j], Student):
                print(rooms[i].room_inside[j].name, rooms[i].room_inside[j].year)
            elif isinstance(rooms[i].room_inside[j], Free_place):
                print(rooms[i].room_inside[j].name)
        print('Количество мест: ', rooms[i].rooms_amount, '  Уровень комфорта в комнате: ', rooms[i].rooms_comfort)
        print('-----------')


def print_rooms(rooms, a):
    a += '\n'
    for i in range(len(rooms)):
        a = a + 'Комната:' + str(rooms[i].ID) + '\n'
        for j in range(rooms[i].rooms_amount):
            if isinstance(rooms[i].room_inside[j], Student):
                a = a + str(rooms[i].room_inside[j].name) + '\n'
            elif isinstance(rooms[i].room_inside[j], Free_place):
                a = a + str(rooms[i].room_inside[j].name) + '\n'
        a = a + 'Количество мест: ' + str(rooms[i].rooms_amount) + '  Уровень комфорта в комнате: ' + str(
            rooms[i].rooms_comfort) + '\n'
        a = a + '-----------' + '\n'
    return a


def temperature_comparison(student_a, student_b, room_comfort):
    comparison = abs(student_a.temperature - student_b.temperature)
    probability = 50
    a = random.randint(1, 100)
    if comparison <= 2:
        probability += 20
    elif comparison >= 5:
        probability -= 20
    else:
        probability += 0

    if 5 >= a - probability > 0:
        room_comfort += 0
    elif a > probability:
        room_comfort -= 5
    elif a <= probability:
        room_comfort += 5
    return room_comfort


def cleaning_comparison(student_a, student_b, room_comfort):
    comparison = abs(student_a.cleaning - student_b.cleaning)
    probability = 50
    a = random.randint(1, 100)
    if comparison == 0:
        probability += 20
    elif comparison == 1:
        probability -= 10
    elif comparison == 2:
        probability -= 20

    if 5 >= a - probability > 0:
        room_comfort += 0
    elif a > probability:
        room_comfort -= 5
    elif a <= probability:
        room_comfort += 5
    return room_comfort


def sound_comparison(student_a, student_b, room_comfort):
    comparison = abs(student_a.sound - student_b.sound)
    probability = 50
    a = random.randint(1, 100)
    if comparison == 0:
        probability += 20
    elif comparison == 1:
        probability -= 10
    elif comparison == 2:
        probability -= 20

    if 5 >= a - probability > 0:
        room_comfort += 0
    elif a > probability:
        room_comfort -= 5
    elif a <= probability:
        room_comfort += 5
    return room_comfort


def hygiene_comparison(student_a, student_b, room_comfort):
    comparison = abs(student_a.hygiene - student_b.hygiene)
    probability = 50
    a = random.randint(1, 100)
    if comparison == 0:
        probability += 20
    elif comparison == 1:
        probability -= 10
    elif comparison == 2:
        probability -= 20
    if 5 >= a - probability > 0:
        room_comfort += 0
    elif a > probability:
        room_comfort -= 5
    elif a <= probability:
        room_comfort += 5
    return room_comfort


def smoking_comparison(student_a, student_b, room_comfort):
    comparison = abs(student_a.smoking - student_b.smoking)
    probability = 50
    a = random.randint(1, 100)
    if comparison == 0:
        probability += 20
    elif comparison == 1:
        probability -= 10
    elif comparison == 2:
        probability -= 20

    if 5 >= a - probability > 0:
        room_comfort += 0
    elif a > probability:
        room_comfort -= 5
    elif a <= probability:
        room_comfort += 5
    return room_comfort


def studies_comparison(student_a, student_b, room_comfort):
    comparison = abs(student_a.studies - student_b.studies)
    probability = 50
    a = random.randint(1, 100)
    if comparison == 0:
        probability += 20
    elif comparison == 1:
        probability += 10
    elif comparison == 2:
        probability += 0
    elif comparison == 3:
        probability -= 10
    elif comparison == 4:
        probability -= 20
    # print(a)
    # print(probability)
    if 5 >= a - probability > 0:
        room_comfort += 0
    elif a > probability:
        room_comfort -= 5
    elif a <= probability:
        room_comfort += 5
    return room_comfort


def loneliness_comparison(student_a, student_b, room_comfort):
    comparison = abs(student_a.loneliness - student_b.loneliness)
    probability = 50
    a = random.randint(1, 100)
    if comparison == 0:
        probability += 20
    elif comparison == 1:
        probability += 10
    elif comparison == 2:
        probability += 0
    elif comparison == 3:
        probability -= 10
    elif comparison == 4:
        probability -= 20

    if 5 >= a - probability > 0:
        room_comfort += 0
    elif a > probability:
        room_comfort -= 5
    elif a <= probability:
        room_comfort += 5
    return room_comfort


def comparison(studentA, studentB, room_comfort):
    a = random.randint(1, 7)
    if a == 1:
        # print('уборка')
        room_comfort = cleaning_comparison(studentA, studentB, room_comfort)
    elif a == 2:
        # print('темпа')
        room_comfort = temperature_comparison(studentA, studentB, room_comfort)
    elif a == 3:
        # print('звук')
        room_comfort = sound_comparison(studentA, studentB, room_comfort)
    elif a == 4:
        # print('один')
        room_comfort = loneliness_comparison(studentA, studentB, room_comfort)
    elif a == 5:
        # print('гигиена')
        room_comfort = hygiene_comparison(studentA, studentB, room_comfort)
    elif a == 6:
        # print('курение')
        room_comfort = smoking_comparison(studentA, studentB, room_comfort)
    elif a == 7:
        # print('учеба')
        room_comfort = studies_comparison(studentA, studentB, room_comfort)
    studentA.comfort += room_comfort
    studentB.comfort += room_comfort
    return room_comfort


def inside_room_communication(room):
    temp = itertools.combinations(room.room_inside, 2)
    for i in list(temp):
        if isinstance(i[0], Student) and isinstance(i[1], Student):
            room.rooms_comfort = comparison(i[0], i[1], room.rooms_comfort)


def super_remove(new_mass, old_mass, room):
    new_mass.append(room)
    old_mass.remove(room)


def find_worst(rooms):
    worst_person_list = []
    for i in range(len(rooms)):
        worst_person = min(rooms[i].room_inside, key=lambda x: x.comfort)
        worst_person_list.append(worst_person)
    return worst_person_list


def bring_room_comfort_to_zero(rooms):
    for el in rooms:
        el.rooms_comfort = 0


def bring_students_comfort_to_zero(rooms):
    for el in rooms:
        for i in range(el.rooms_amount):
            el.room_inside[i].comfort = 0


def giga_swap(worst_people, rooms):
    free_place_count = 0
    while len(worst_people) != 0:
        if len(worst_people) == 1:
            for room in rooms:
                if worst_people[0] in room.room_inside:
                    f_index_person = room.room_inside.index(worst_people[0])
                    f_index_room = rooms.index(room)
            for i in range(len(rooms)):
                for j in range(rooms[i].rooms_amount):
                    if isinstance(rooms[i].room_inside[j], Free_place):
                        free_place_count += 1
                        s_index_person = j
                        s_index_room = i
            worst_people.pop(0)
            if free_place_count > 0:
                if s_index_room != f_index_room:
                    rooms[f_index_room].room_inside[f_index_person], rooms[s_index_room].room_inside[s_index_person] = \
                        rooms[s_index_room].room_inside[s_index_person], rooms[f_index_room].room_inside[f_index_person]
            else:
                return (rooms)
        else:
            if len(worst_people) == 1:
                break
            for room in rooms:
                if worst_people[0] in room.room_inside:
                    f_index_person = room.room_inside.index(worst_people[0])
                    f_index_room = rooms.index(room)
                    # print('fffffffff',f_index_room)
                if worst_people[1] in room.room_inside:
                    s_index_person = room.room_inside.index(worst_people[1])
                    s_index_room = rooms.index(room)
                    # print('ssssssssss', s_index_room)
            rooms[f_index_room].room_inside[f_index_person], rooms[s_index_room].room_inside[s_index_person] = \
                rooms[s_index_room].room_inside[s_index_person], rooms[f_index_room].room_inside[f_index_person]
            worst_people.pop(0)
            worst_people.pop(0)


def extract_perfect_rooms(rooms):
    ideal_rooms = []
    len_rooms = len(rooms)
    temp = 0
    while len(rooms) > 0:
        for i in range(len(rooms)):
            for j in range(5):
                inside_room_communication(rooms[i])
        for el in rooms:
            if el.rooms_comfort > 15:
                super_remove(ideal_rooms, rooms, el)
        # print('Хорошие комнаты')
        # print_rooms(ideal_rooms)
        if len(rooms) > 0:
            worst_people = find_worst(rooms)
            giga_swap(worst_people, rooms)
            # print('Плохие комнаты')
            # print_rooms(rooms)
            bring_room_comfort_to_zero(rooms)
            bring_students_comfort_to_zero(rooms)
        if len_rooms == len(rooms):
            # print('Те же')
            temp += 1
        else:
            # print('Другие')
            temp = 0
            len_rooms = len(rooms)
        if temp == 3:
            return ideal_rooms, rooms
    return ideal_rooms, rooms


def creation_of_none_students(rooms):
    for i in range(len(rooms)):
        for j in range(rooms[i].rooms_amount):
            if rooms[i].room_inside[j] == 0:
                rooms[i].room_inside[j] = Free_place()


def choose_file():
    clear_text()
    file_path = filedialog.askopenfilename()
    return file_path


def clear_text():
    text_box.delete('1.0', tk.END)
    #text_box.config(height=1, width=50)
    text_box1.delete('1.0', tk.END)
    #text_box1.config(height=1, width=50)
def process_file(file_path, rooms):
    students_attributes = agents_from_excel(file_path)

    students_list = agents_creation(students_attributes)
    refractor(students_list)

    male_students, female_students = sex_pool(students_list)
    amount_of_male_students = len(male_students)
    amount_of_female_students = len(female_students)

    count_for_amount_of_male_students = amount_of_male_students
    count_for_amount_of_female_students = amount_of_female_students

    male_rooms = []
    female_rooms = []
    k = 0
    rooms = rooms_creation(rooms)
    # print(rooms)
    while count_for_amount_of_male_students > 0 or count_for_amount_of_female_students > 0:
        if count_for_amount_of_male_students <= 0:
            pass
        else:
            if count_for_amount_of_male_students - rooms[k].rooms_amount >= 0:
                male_rooms.append(rooms[k])
                count_for_amount_of_male_students -= rooms[k].rooms_amount
                rooms.pop(0)
            else:
                if rooms.count(count_for_amount_of_male_students - rooms[k].rooms_amount):
                    for i in range(len(rooms)):
                        if rooms[i] == count_for_amount_of_male_students - rooms[k].rooms_amount:
                            male_rooms.append(rooms[i])
                            count_for_amount_of_male_students -= rooms[k].rooms_amount
                            rooms.pop(i)
                            break
                else:
                    male_rooms.append(rooms[-1])
                    count_for_amount_of_male_students -= rooms[k].rooms_amount
                    rooms.pop(-1)
        if count_for_amount_of_female_students <= 0:
            pass
        else:
            if count_for_amount_of_female_students - rooms[k].rooms_amount >= 0:
                female_rooms.append(rooms[k])
                count_for_amount_of_female_students -= rooms[k].rooms_amount
                rooms.pop(0)
            else:
                if rooms.count(count_for_amount_of_female_students - rooms[k].rooms_amount):
                    for i in range(len(rooms)):
                        if rooms[i] == count_for_amount_of_female_students - rooms[k].rooms_amount:
                            female_rooms.append(rooms[i])
                            count_for_amount_of_female_students -= rooms[k].rooms_amount
                            rooms.pop(i)
                            break
                else:
                    female_rooms.append(rooms[-1])
                    count_for_amount_of_female_students -= rooms[k].rooms_amount
                    rooms.pop(-1)

    students_check_in(male_students, male_rooms)
    students_check_in(female_students, female_rooms)
    creation_of_none_students(male_rooms)
    creation_of_none_students(female_rooms)
    a = 'Комнаты с высоким уровнем комфрта:'
    b = 'Комнаты с низким уровнем комфрта:'
    perfect_male_rooms, male_rooms = extract_perfect_rooms(male_rooms)
    perfect_female_rooms, female_rooms = extract_perfect_rooms(female_rooms)
    result1 = print_rooms(perfect_male_rooms, a)
    result2 = print_rooms(male_rooms, b)
    result3 = print_rooms(perfect_female_rooms, a)
    result4 = print_rooms(female_rooms, b)
    if result2 == (b + '\n'):
        resultM = result1 + '\n'
    else:
        resultM = result1 + '\n' + result2

    if result4 == (b + '\n'):
        resultF= result3 + '\n'
    else:
        resultF = result3 + '\n' + result4
    return [resultM, resultF]


def on_text_changed(event):
    # получаем количество строк и символов в тексте
    num_lines = text_box.index('end-1c').split('.')[0]
    num_chars = 50
    text_box.config(height=num_lines, width=num_chars + 2)
    num_lines = text_box1.index('end-1c').split('.')[0]
    num_chars = 50
    text_box1.config(height=num_lines, width=num_chars + 2)


def display_result(resultM,resultF):
    text_box.insert(tk.END, resultM)
    text_box1.insert(tk.END, resultF)


# создаем графический интерфейс
root = tk.Tk()
root.geometry('1290x1400')
# загружаем изображение
#root.config(bg="light blue")
# загружаем изображение
bg_image = tk.PhotoImage(file="background.gif")

# устанавливаем фоновое изображение
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)
# создаем метку для вывода результата
label = tk.Label(root, text="Выберите файл для обработки", font=("Arial", 20),fg='#ffffff',bg = '#2591d9')
label0 = tk.Label(root, bg="black")
label1 = tk.Label(root, bg="black")

label0.grid(column=0, row=0)
label1.grid(column=2, row=0)

label0.grid_forget()
label1.grid_forget()

label.grid(column=1, row=0)
text_box = ScrolledText(root)
text_box.grid(column=0, row=2, padx=10, pady=10)
text_box.config(height=1, width=50)
text_box.bind('<<Modified>>', on_text_changed)
label_male = tk.Label(root, text="Мужские комнаты", fg='#ffffff',font=("Arial", 14), bg = '#2591d9',padx=10, pady=10)
label_female = tk.Label(root, text="Женские комнаты", fg='#ffffff',font=("Arial", 14), bg = '#2591d9', padx=10, pady=10)
label_male.grid(column=0, row=1, padx=10, pady=10)
label_female.grid(column=3, row=1, padx=10, pady=10)

label_zero = tk.Label(root,bg = '#2591d9', padx=10, pady=10)
label_zero.grid(column=1, row=1, padx=10, pady=10)


text_box1 = ScrolledText(root)
text_box1.grid(column=3, row=2, padx=10, pady=10)
text_box1.config(height=1, width=50)
text_box1.bind('<<Modified>>', on_text_changed)
file_button = tk.Button(root, text="Выбрать файл", command=lambda: display_result(*process_file(choose_file(), rooms)),
                        font=("Arial", 12), height=2, width=20, padx=10, pady=20)
file_button.grid(column=1, row=1)
clear_button = tk.Button(root, text='Очистить поле', command=clear_text, font=("Arial", 12), height=2, width=20,
                         padx=10, pady=20)
clear_button.grid(column=1, row=2, padx=10, pady=10)

root.mainloop()
