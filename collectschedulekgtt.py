from recipientgsheets import RecipientGoogleSheets
import pandas as pd
from PIL import Image,ImageDraw,ImageFont

def text_size(list_subjects, font):

    font = font
    if [s for s in list_subjects if '\n' in s]:
        for i in list_subjects:
            if i == (x:=[s for s in list_subjects if '\n' in s][0]):
                index = list_subjects.index(x)
                list_subjects[index] = i.split('\n')
                break
        form_list = []
        for i in list_subjects:
            if isinstance(i,list):
                for y in i:
                    form_list.append(y)
            else:
                form_list.append(i)
        for i in form_list:
            if i.startswith(' '):
                form_list[form_list.index(i)] = f'(#) {i.lstrip()}'
    else:
        form_list = list_subjects[:]

    length =(font.getsize(max(form_list,key=len))[0])
    height = [font.getsize(text)[1] for text in form_list]
    return sum(height)-10,length+10

def center(*args:str):
    temp_list = [*args]
    very_long = int(len(max(temp_list,key=len))/2)
    new =[]
    for i in range(len(temp_list)):
        cent = very_long - int(len(temp_list[i])/2)
        stroke = f'{cent*" "}{temp_list[i]}'
        new.append(stroke)
    return "\n".join(new)

def get_groups_list() -> list:
    timetable = RecipientGoogleSheets('1rGJ4_4BbSm0qweN7Iusz8d55e6uNr6bFRCv_j3W5fGU')
    temp_list = []
    for i in (1, 7, 13, 19):
        column = timetable.get_column(i)
        for y in column:
            if y.isupper() and y not in ('КЛАССНЫЙ ЧАС', 'ОБЖ') or y in ('ОПИр-21-9', 'ОПИр-22-9', 'ОПИр-20-9'):
                temp_list.append(y)
    return temp_list

def get_time(classhour = None):

    if classhour is None:
        time_without_classhour = ['08:30 - 10:00',
                '10:10 - 11:40',
                '11:50 - 13:20',
                '13:30 - 15:00',
                '15:10 - 16:40',
                '16:45 - 18:15']
        return time_without_classhour

    else:

        time_with_classhour = ['08:30 - 10:00',
                                '10:10 - 11:40',
                                '11:50 - 12:20',
                                '12:30 - 14:00',
                                '14:10 - 15:40',
                                '16:50 - 17:20']
        return time_with_classhour

class Scavanger:

    def __init__(self,group:str):

        self.group = group
        self.timetable = RecipientGoogleSheets('1rGJ4_4BbSm0qweN7Iusz8d55e6uNr6bFRCv_j3W5fGU')
        self.timetable_date = self.timetable.get_line(0)[0][9:33]
        self.column_index = self.__column_index()

        self.lesson=self.timetable.get_column(self.column_index)

        self.up_cut = self.lesson.index(self.group)

        exception_group = self.__exception_groups()

        if self.group in exception_group:
            self.down_cut = self.lesson.index(f'{self.group}') + 11

        else:
            keys = self.__groups_dictionary()
            self.down_cut = self.lesson.index(keys[f'{self.group}'])

    def __filtering(self,subjects_list):

        temp_list = [s for s in subjects_list if '[]  - '.lower() in s.lower()]
        for i in temp_list:
            index = subjects_list.index(i)
            subjects_list[index] = f'({index + 1}) — — — —'

        temp_list = [s for s in subjects_list if '[] И'.lower() in s.lower()]
        for i in temp_list:
            index = subjects_list.index(i)
            subjects_list[index] = f'({index + 1}) {i[7:]}'

        temp_list = [s for s in subjects_list if 'Чудакова'.lower() in s.lower()]
        for i in temp_list:
            index = subjects_list.index(i)
            subjects_list[index] = f'({index + 1}) {i[7:]}'

        return subjects_list

    def __add_timer(self,subjects):
        classhour = [s for s in subjects if 'КЛАССНЫЙ ЧАС'.lower() in s.lower()]
        global time
        if classhour:
            time = get_time(None)

        if not classhour:
            time = get_time(1)

        for i in subjects:
            index = subjects.index(i)
            subjects[index] = "{" + time[index] + "} " + i

        return subjects

    def __cabinets(self)->list:
        _cabinet = self.timetable.get_column(self.column_index + 4)
        _cabinet = _cabinet[self.up_cut:self.down_cut][1:]

        if len(_cabinet) in (1,3,5,7,9,11):
            _cabinet.insert(0, '')

        cabinet = []
        for index in range(0, len(_cabinet), 2):
            cabinet.append(f'{_cabinet[index]}')
        return cabinet

    def __subjects(self)-> list:

        _lesson = self.lesson[self.up_cut:self.down_cut][1:]
        _second_lesson = self.timetable.get_column(self.column_index + 2)
        _second_lesson = _second_lesson[self.up_cut:self.down_cut][1:]

        if len(_lesson) and len(_second_lesson) in (1,3,5,7,9,11):
            _lesson.insert(0,''),_second_lesson.insert(0,'')

        lessons = []
        second_lessons = []
        for i in range(0, len(_lesson), 2):
            lessons.append(_lesson[i])
            second_lessons.append(f'{_second_lesson[i]} - {_second_lesson[i + 1]}')

        for lesson,second_lesson,index in zip(lessons,second_lessons,enumerate(lessons)):
            if lesson.startswith('Иностранный язык' or 'Инжинерная'):
                if second_lesson != ' - ':
                    lessons[index[0]] = f'{lesson}\n {36 * " "}{second_lesson}'

        return lessons

    def __groups_dictionary(self) -> dict:
        temp_list = []
        for i in (1, 7, 13, 19):
            column = self.timetable.get_column(i)
            for y in column:
                if y.isupper() and y not in ('КЛАССНЫЙ ЧАС', 'ОБЖ') or y in ('ОПИр-21-9', 'ОПИр-22-9', 'ОПИр-20-9'):
                    temp_list.append(y)
                    temp_list.append(y)
        temp_list = temp_list[1:-1]
        return dict(zip(temp_list[::2], temp_list[1::2]))

    def __exception_groups(self) -> list:
        exception_groups = []
        for i in (1, 7, 13, 19):
            column = self.timetable.get_column(i)
            group = [i for i in column if i.isupper()][-1]
            exception_groups.append(group)
        return exception_groups

    def __column_index(self)-> int:
            df = pd.read_csv('https://docs.google.com/spreadsheets/d/1rGJ4_4BbSm0qweN7Iusz8d55e6uNr6bFRCv_j3W5fGU/gviz/tq?tqx=out:csv&sheet')
            sought_line = [line for line in df.values if f'{self.group}' in line][0].tolist()
            return sought_line.index(self.group)

    def __teachers(self) -> list:
        _lesson = self.lesson[self.up_cut:self.down_cut][1:]
        if len(_lesson) in (1, 3, 5, 7, 9, 11):
            _lesson.insert(0, '')

        teachers = [_lesson[i + 1] for i in range(0, len(_lesson), 2)]

        return teachers

    def ready_schedule(self):
        schedule = self.__subjects()

        if all([i == '' for i in schedule]):
            return 'Расписния нет, приятного отдыха!'

        else:
            cabinet = self.__cabinets()
            num = [i for i in range(1, len(cabinet)+1)]

            subjects = []
            for i in range(0, len(schedule)):
                result = f'({num[i]}) [{cabinet[i]}] {schedule[i]}'
                subjects.append(result)

            self.__filtering(subjects)
            self.__add_timer(subjects)

            return subjects



    def get_information(self):
        return center(self.timetable_date,self.group)

    def get_image(self):
        font = ImageFont.truetype('cl.ttf', size=40)
        lines = self.ready_schedule()
        print(lines)
        # if all(' ' in lines) :
        #     text = lines
        #     height, length = text_size(text, font)
        #     image = Image.new('RGBA', (length + 50, height + 30), '#282830')
        #     idraw = ImageDraw.Draw(image)
        #     idraw.text((15, 25), f'{text}', font=font)
        #     image.save('image.png')
        #     image.show()


        # else:
        #     text = f'\n'.join(lines)
        #     list = lines[:]
        #     height,length=text_size(list,font)
        #     image = Image.new('RGBA', (length+50, height+30), '#282830')
        #     idraw = ImageDraw.Draw(image)
        #     idraw.text((15, 25), f'{text}', font=font)
        #     image.save('image.png')
        #     image.show()

    def tester(self):
        print(len(get_groups_list()))

if __name__ == '__main__':
    # x = Scavanger('1ИСИП-21-9')
    x = Scavanger('1ОГР-21-9')
    print(x.ready_schedule())