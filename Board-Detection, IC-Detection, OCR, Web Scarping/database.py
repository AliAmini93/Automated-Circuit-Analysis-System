import logging

logger = logging.getLogger('logger_Info')
logger_Debug = logging.getLogger('logger_Debug')
from pymongo import MongoClient
import os
from ic_info.path import Path_Datasheets, Path_Images, Path_Input
import shutil


def db_connection():
    client = MongoClient()

    db = client['ic4']
    collection_name = db["icdetails4"]

    # item_details = collection_name.find()
    # for item in item_details:
    # This does not give a very readable output
    # pprint.pprint(item)
    return collection_name


collection_name = db_connection()


def delete_mongodb(key, value):
    data_IC = collection_name.find_one({key: value})
    if data_IC != None:
        collection_name.delete_many({key: value})
        _id = data_IC['_id']
        try:
            os.remove(Path_Datasheets + str(_id) + '.pdf')
            os.remove(Path_Images + str(_id))
        except Exception as e:
            logger_Debug.exception(str(e))
            print('datasheet does not exist')
        print('IC removed')
    else:
        print('IC not exist in database')


def insert_mongodb(data_IC, pic):
    source = data_IC['source']
    DataSheetUrl = data_IC['DataSheetUrl']
    _id = collection_name.insert_one(data_IC)

    logger.info('DataSheetUrl: %s ' % DataSheetUrl)
    pic_new_name = str(_id.inserted_id) + '.' + pic.split('.')[-1]
    shutil.copy(Path_Input + pic, Path_Images + pic_new_name)

    result = ''
    if DataSheetUrl != '-' and (source == 'alldatasheet' or source == 'alldatasheet_manufacturer' or source == 'user'):
        result = os.rename(DataSheetUrl, Path_Datasheets + str(_id.inserted_id) + '.pdf')

    elif source == 'Texas Instruments' or source == 'mouser':
        result = os.system(
            'wget {} -O {} --timeout=10 --tries=10'.format(DataSheetUrl,
                                                           Path_Datasheets + str(_id.inserted_id) + '.pdf'))

    if result == 0 or result == None:
        data_IC['DataSheetUrl'] = ''
        collection_name.update_one({'_id': _id.inserted_id}, {'$set': {'DataSheetUrl': ''}})


def update_mongodb(data_IC, pic):
    if data_IC['DataSheetUrl'] != '' and data_IC['DataSheetUrl'].startswith("http") == False and data_IC[
        'DataSheetUrl'] != '-':
        if os.path.isfile(Path_Datasheets + str(data_IC['_id']) + '.pdf'):
            os.remove(Path_Datasheets + str(data_IC['_id']) + '.pdf')
        os.rename(data_IC['DataSheetUrl'], Path_Datasheets + str(data_IC['_id']) + '.pdf')
        data_IC['DataSheetUrl'] = ''
    collection_name.update_one({'_id': data_IC['_id']}, {'$set': data_IC})


def change_database(data, pictures_IC):
    delete_IC = []
    delete_pic = []
    for d, pic in zip(data, pictures_IC):
        if d['flag'] == 1 and d['ManufacturerPartNumber'] != 'پیدا نشد':
            if '_id' not in d.keys():
                insert_mongodb(d, pic)
            else:
                update_mongodb(d, pic)
        if d['flag'] == 2:
            if '_id' in d.keys():
                delete_mongodb('_id', d['_id'])
            delete_IC.append(d)
            delete_pic.append(pic)

    for i, p in zip(delete_IC, delete_pic):
        data.remove(i)
        pictures_IC.remove(p)
    return data, pictures_IC
