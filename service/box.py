import datetime
import re

from fastapi import HTTPException
from pydantic import BaseModel, validator


class Box(BaseModel):
    name: str
    make_date: str

    @validator('make_date')
    def validate_make_date(cls, date):
        if not bool(re.match('^\d{4}-\d{2}-\d{2}$', date)):
            raise HTTPException(status_code=400, detail={'field': 'make_date', 'msg': 'Не правильный формат даты'})
        if not datetime.datetime.now() - datetime.timedelta(days=365) < datetime.datetime.strptime(date, '%Y-%m-%d') < datetime.datetime.now():
            raise HTTPException(status_code=400, detail={'field': 'make_date', 'msg': 'Не правильный диапазон'})
        return date

    @validator('name')
    def validate_name(cls, name):
        if not 5 <= len(name) <= 30:
            raise HTTPException(status_code=400, detail={'field': 'name', 'msg': 'Не верная длина поля'})
        regex = re.compile(r'[а-яА-ЯёЁ ]')
        for i in name:
            if bool(regex.search(i)):
                continue
            else:
                raise HTTPException(
                    status_code=400, detail={'field': 'name',
                                             'msg': 'Имя должно состоять только из русских символов и пробелов'})
        return name
