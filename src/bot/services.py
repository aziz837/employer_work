from django.db import connections

def getOwners(category_id, region_id, district_id):
    with connection.cursor() as cursor:
        cursor.execute(""" SELECT tg_id 
                from bot_user bu 
                inner join 
                    (select user_id_id from bot_usercategory where cat_id_id=%s GROUP by user_id_id) as user_cats 
                    on bu.id = user_cats.user_id_id
                inner join 
                    (select user_id from bot_userregion where region_id=%s and district_id =%s GROUP by user_id ) as user_regions 
                    on bu.id = user_regions.user_id""", [category_id, region_id, district_id])
        row = cursor.fetchone()
    return row