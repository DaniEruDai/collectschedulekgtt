from recipientgsheets import RecipientGoogleSheets
import pandas as pd

def center(*args:str):
    temp_list = [*args]
    very_long = int(len(max(temp_list,key=len))/2)
    new =[]
    for i in range(len(temp_list)):
        cent = very_long - int(len(temp_list[i])/2)
        stroke = f'{cent*" "}{temp_list[i]}'
        new.append(stroke)
    return "\n".join(new)

def get_all_groups() -> list:
    timetable = RecipientGoogleSheets('1rGJ4_4BbSm0qweN7Iusz8d55e6uNr6bFRCv_j3W5fGU')
    temp_list = []
    for i in [1, 7, 13, 19]:
        target = timetable.get_column(i)
        for y in target:
            if y.isupper():
                temp_list.append(y)
            elif y == 'ОПИр-21-9':
                temp_list.append(y)

            elif y == 'ОПИр-22-9':
                temp_list.append(y)

            elif y == 'ОПИр-20-9':
                temp_list.append(y)

    for _ in range(temp_list.count('ОБЖ')):
        temp_list.remove('ОБЖ')

    return temp_list

class Collector:

    def dictionary(self) -> dict:
        dictionary = {}
        temp_list = []
        for i in [1, 7, 13, 19]:
            target =self.timetable.get_column(i)
            for y in target:
                if y.isupper():
                    if y != 'КЛАССНЫЙ ЧАС':
                        temp_list.append(y)
                        temp_list.append(y)
                elif y == 'ОПИр-21-9':
                    temp_list.append(y)
                    temp_list.append(y)

                elif y == 'ОПИр-22-9':
                    temp_list.append(y)
                    temp_list.append(y)

                elif y =='ОПИр-20-9':
                    temp_list.append(y)
                    temp_list.append(y)


        temp_list.pop(0)
        temp_list.pop(-1)
        for _ in range(temp_list.count('ОБЖ')):
            temp_list.remove('ОБЖ')
        for index in range(0, len(temp_list) - 1, 2):
            dictionary[temp_list[index]] = temp_list[index + 1]
        return dictionary

    def exception_group(self) -> list:
        exception_group = []
        for i in [1, 7, 13, 19]:
            temp_list = []
            column = self.timetable.get_column(i)
            for _ in range(column.count('ОБЖ')):
                column.remove('ОБЖ')
            for ellement in column:
                if ellement.isupper():
                    temp_list.append(ellement)
                elif ellement == 'ОПИр-21-9':
                    temp_list.append(ellement)
            exception_group.append(temp_list[-1])
        return exception_group

    def __init__(self,group:str):

        self.group = group
        self.timetable = RecipientGoogleSheets('1rGJ4_4BbSm0qweN7Iusz8d55e6uNr6bFRCv_j3W5fGU')



        self.lesson=self.timetable.get_column(self.get_column_index())

        self.up_cut = self.lesson.index(self.group)

        exception_group = self.exception_group()

        if self.group in exception_group:
            self.down_cut = self.lesson.index(f'{self.group}') + 11
        else:
            keys = self.dictionary()

            self.down_cut = self.lesson.index(keys[f'{self.group}'])

    def get_column_index(self)-> int:

        URL = f'https://docs.google.com/spreadsheets/d/1rGJ4_4BbSm0qweN7Iusz8d55e6uNr6bFRCv_j3W5fGU/gviz/tq?tqx=out:csv&sheet'
        df = pd.read_csv(URL)

        X = []
        for line in df.values:
            result_line = [str(y) for y in line]
            for ellement in result_line:

                if 'nan' in result_line:
                    for _ in range(result_line.count('nan')):
                        index = result_line.index('nan')
                        result_line[index] = ''

                if ellement.endswith('.0'):
                    result_line[result_line.index(ellement)] = ellement[:-2]

            X.append(result_line)
        temp_list = [s for s in X if f'{self.group}' in s]
        for i in temp_list:
            index_column = i.index(f'{self.group}')

            return index_column

    def get_schedule(self)-> list:

        _lesson = self.lesson
        _lesson = _lesson[self.up_cut:self.down_cut][1:]

        _second_lesson = self.timetable.get_column(self.get_column_index() + 2)
        _second_lesson = _second_lesson[self.up_cut:self.down_cut][1:]



        if len(_lesson) and len(_second_lesson) == 7:
            _lesson.insert(0,'')
            _second_lesson.insert(0,'')

        if len(_lesson) and len(_second_lesson) == 11:
            _lesson.insert(0,'')
            _second_lesson.insert(0,'')

        if len(_lesson) and len(_second_lesson) == 9:
            _lesson.insert(0,'')
            _second_lesson.insert(0,'')

        if len(_lesson) and len(_second_lesson) == 5:
            _lesson.insert(0,'')
            _second_lesson.insert(0,'')

        if len(_lesson) and len(_second_lesson) == 3:
            _lesson.insert(0,'')
            _second_lesson.insert(0,'')

        if len(_lesson) and len(_second_lesson) == 1:
            _lesson.insert(0,'')
            _second_lesson.insert(0,'')

        list_subjects = []
        lesson = []

        for i in range(0, len(_lesson), 2):
            list_subjects.append(f'{_lesson[i]} - {_lesson[i + 1]}')

        for i in range(0, len(_lesson), 2):
            lesson.append(f'{_second_lesson[i]} - {_second_lesson[i + 1]}')

        for i in list_subjects:
            if i.startswith('Иностранный язык'):
                for y in lesson:
                    if y.startswith('Иностранный язык'):
                        index = list_subjects.index(i)
                        list_subjects[index] = f'{i}\n    {lesson[index]}'

        for i in list_subjects:
            if i == ' - ':
                index = [i for i, ltr in enumerate(list_subjects) if ltr == ' - ']
                for z in index:
                    list_subjects[z] = lesson[z]

        return list_subjects

    def get_cabinet(self)->list:
        _cabinet = self.timetable.get_column(self.get_column_index() + 4)
        _cabinet = _cabinet[self.up_cut:self.down_cut][1:]

        if len(_cabinet) == 1:
            _cabinet.insert(0, '')

        if len(_cabinet) == 3:
            _cabinet.insert(0, '')

        if len(_cabinet) == 5:
            _cabinet.insert(0, '')

        if len(_cabinet) == 7:
            _cabinet.insert(0,'')

        if len(_cabinet) == 9:
                _cabinet.insert(0, '')

        if len(_cabinet) == 11:
            _cabinet.insert(0, '')


        cabinet = []
        for i in range(0, len(_cabinet), 2):
            cabinet.append(f'{_cabinet[i]}')
        return cabinet

    def update_schedule(self)-> str:
        timetable_date = self.timetable.get_line(0)[0][9:33]
        schedule = self.get_schedule()

        terms = all([i == ' - ' for i in schedule])
        if terms:
            str1 = 'Расписния нет,'
            str2 = 'приятного отдыха!'
            string = self.group+ "\n"
            return f'{center(timetable_date,string,str1,str2)}'

        else:
            cabinet = self.get_cabinet()
            num = [i for i in range(1, len(cabinet)+1)]

            public = []
            for i in range(0, len(schedule)):
                i = f'({num[i]}) [{cabinet[i]}] {schedule[i]}'
                public.append(i)

            temp_list = [s for s in public if '[]  - '.lower() in s.lower()]
            for i in temp_list:
                index = public.index(i)
                public[index] = f'({index + 1}) --------'

            temp_list = [s for s in public if '[] И'.lower() in s.lower()]
            for i in temp_list:
                index = public.index(i)
                public[index] = f'({index + 1}) {i[7:]}'


            return f'{center(timetable_date,self.group)}\n\n' + '\n'.join(public)








