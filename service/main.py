import re
import uuid
from datetime import datetime

from fastapi import FastAPI, HTTPException

from box import Box

app = FastAPI()

local_storage = [
    {'guid': '2f11868c-a367-48dc-b4d1-c6706f5258f4', 'name': 'Красивая коробка номер', 'make_date': '2021-10-15'}
]


@app.post('/api/box')
def save(box: Box):
    for box_in_storage in local_storage:
        if box.name == box_in_storage['name']:
            raise HTTPException(status_code=400,
                                detail={'field': 'name', 'msg': 'Коробка с таким именем уже есть в базе'})
    guid = str(uuid.uuid4())
    local_storage.append({
        'guid': guid,
        'name': box.name,
        'make_date': box.make_date
    })
    print(local_storage)
    return guid


@app.get('/api/box/{box_id}')
def get(box_id):
    if re.match('^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$', box_id):
        for box in local_storage:
            if box['guid'] == box_id:
                return {
                    'guid': box['guid'],
                    'name': box['name'],
                    'age_days': (datetime.now() - datetime.strptime(box['make_date'], '%Y-%m-%d')).days
                }
        else:
            raise HTTPException(status_code=404, detail=f"Коробка с с идентификатором {box_id} не найдена")
    else:
        raise HTTPException(status_code=400, detail="Неверный формат идентификатора")


@app.delete('/api/box/{box_id}', status_code=200)
def delete(box_id):
    if re.match('^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$', box_id):
        for box in local_storage:
            if box['guid'] == box_id:
                local_storage.remove(box)
                return
        raise HTTPException(status_code=404)
    else:
        raise HTTPException(status_code=400)
