from recipientgsheets import RecipientGoogleSheets
import pandas as pd
from PIL import Image,ImageDraw,ImageFont
import datetime

def get_text_size(list_subjects, font):

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

def get_time(length,index_classroom = None):
    start_time,classroom, school_break, thclass = ('08:30','00:30', '00:10', '01:30')
    if index_classroom:
        stage_1 = [thclass for _ in range(length)]
        stage_1[index_classroom-1] = classroom
        for i in range(1,length*2-1,2):
            stage_1.insert(i,school_break)
    elif index_classroom is None:
        stage_1 = [thclass for _ in range(0, length)]
        for i in range(1, length * 2 - 1, 2):
            stage_1.insert(i, school_break)
        if length == 6 :
            stage_1[9] = '00:05'
    hours_1,minutes_1 = map(int,(start_time[0:2],start_time[3:]))
    start_time = datetime.timedelta(hours=hours_1,minutes=minutes_1)
    stage_2 = [datetime.timedelta(hours = int(i[:2]) , minutes = int(i[3:])) for i in stage_1]
    for i in stage_2:
        start_time = start_time + i
        stage_2[stage_2.index(i)] = str(start_time)[:-3]
    stage_2.insert(0, '08:30')
    time = [stage_2[i] for i in range(0,len(stage_2),2)]
    time = []
    for i in range(0, len(stage_2), 2):
        time.append(f'{stage_2[i]} - {stage_2[i + 1]}')
    return time

class Collector:

    def __init__(self,group:str):

        self.group = group
        self.timetable = RecipientGoogleSheets('1rGJ4_4BbSm0qweN7Iusz8d55e6uNr6bFRCv_j3W5fGU')
        self.timetable_date = self.timetable.get_line(0)[0][9:33]

        self.lesson=self.timetable.get_column(self.get_column_index())

        self.up_cut = self.lesson.index(self.group)

        exception_group = self.get_exception_groups()

        if self.group in exception_group:
            self.down_cut = self.lesson.index(f'{self.group}') + 11
        else:
            keys = self.get_groups_dictionary()
            self.down_cut = self.lesson.index(keys[f'{self.group}'])

    def get_groups_dictionary(self) -> dict:
        temp_list = []
        for i in (1, 7, 13, 19):
            column = self.timetable.get_column(i)
            for y in column:
                if y.isupper() and y not in ('КЛАССНЫЙ ЧАС', 'ОБЖ') or y in ('ОПИр-21-9', 'ОПИр-22-9', 'ОПИр-20-9'):
                    temp_list.append(y)
                    temp_list.append(y)
        temp_list = temp_list[1:-1]
        return dict(zip(temp_list[::2], temp_list[1::2]))

    def get_exception_groups(self) -> list:
        exception_groups = []
        for i in (1, 7, 13, 19):
            column = self.timetable.get_column(i)
            group = [i for i in column if i.isupper()][-1]
            exception_groups.append(group)
        return exception_groups

    def get_column_index(self)-> int:
            df = pd.read_csv('https://docs.google.com/spreadsheets/d/1rGJ4_4BbSm0qweN7Iusz8d55e6uNr6bFRCv_j3W5fGU/gviz/tq?tqx=out:csv&sheet')
            sought_line = [line for line in df.values if f'{self.group}' in line][0].tolist()
            return sought_line.index(self.group)

    def get_subjects_list(self)-> list:

        _lesson = self.lesson[self.up_cut:self.down_cut][1:]
        _second_lesson = self.timetable.get_column(self.get_column_index() + 2)
        _second_lesson = _second_lesson[self.up_cut:self.down_cut][1:]

        if len(_lesson) and len(_second_lesson) in (1,3,5,7,9,11):
            _lesson.insert(0,''),_second_lesson.insert(0,'')

        lessons = []
        second_lessons = []
        for i in range(0, len(_lesson), 2):
            lessons.append(f'{_lesson[i]} - {_lesson[i + 1]}')
            second_lessons.append(f'{_second_lesson[i]} - {_second_lesson[i + 1]}')

        for lesson,second_lesson,index in zip(lessons,second_lessons,enumerate(lessons)):
            if lesson.startswith('Иностранный язык' or 'Инжинерная'):
                if second_lesson != ' - ':
                    lessons[index[0]] = f'{lesson}\n {36 * " "}{second_lesson}'

        return lessons

    def get_cabinet(self)->list:
        _cabinet = self.timetable.get_column(self.get_column_index() + 4)
        _cabinet = _cabinet[self.up_cut:self.down_cut][1:]

        if len(_cabinet) in (1,3,5,7,9,11):
            _cabinet.insert(0, '')

        cabinet = []
        for index in range(0, len(_cabinet), 2):
            cabinet.append(f'{_cabinet[index]}')
        return cabinet

    def get_ready_schedule(self)-> str:
        timetable_date = self.timetable_date
        schedule = self.get_subjects_list()

        if all([i == ' - ' for i in schedule]):
            str1 = 'Расписния нет, приятного отдыха!'
            group = self.group+ "\n"
            return f'{center(timetable_date,group,str1)}'

        else:
            cabinet = self.get_cabinet()
            num = [i for i in range(1, len(cabinet)+1)]

            public = []
            for i in range(0, len(schedule)):
                result = f'({num[i]}) [{cabinet[i]}] {schedule[i]}'
                public.append(result)

            temp_list = [s for s in public if '[]  - '.lower() in s.lower()]
            for i in temp_list:
                index = public.index(i)
                public[index] = f'({index + 1}) — — — —'

            temp_list = [s for s in public if '[] И'.lower() in s.lower()]
            for i in temp_list:
                index = public.index(i)
                public[index] = f'({index + 1}) {i[7:]}'

            full_classtime = [s for s in public if 'КЛАССНЫЙ ЧАС'.lower() in s.lower()]
            if full_classtime in public:
                index_classroom = public.index(full_classtime)

            else:
                index_classroom = None

            time = get_time(length=len(public),index_classroom=index_classroom)

            for i in public:
                index = public.index(i)
                public[index] = "{"+time[index]+"} " + i

            return public

    def get_timetable_date(self):
        return self.timetable_date

    def get_image(self):
        font = ImageFont.truetype('Clear.ttf', size=40)
        lines = self.get_ready_schedule()
        text = f'\n'.join(lines)
        list = lines[:]
        height,length=get_text_size(list,font)
        image = Image.new('RGBA', (length+50, height+30), '#282830')
        idraw = ImageDraw.Draw(image)
        idraw.text((15, 25), f'{text}', font=font)
        image.save('image.png')
