from configs.configs import engine
from services.module.inventory.inventory_model import inventory
from sqlalchemy import select, insert
from datetime import datetime
from sqlalchemy.orm import sessionmaker
# from helpers.validator import validate_data
from helpers.generator import get_UUID
from helpers.validator import validate_data

Session = sessionmaker(bind=engine)

async def post_inventory_query(data:dict):
    session = Session() 

    try: 
        # Query builder
        # query_select = select(user.c.id).where(user.c.id == data.('created_by'))
        # result_select = session.execute(query_select)
        # check_user = result_select.first()

        # if check_user:
            # Command builder
            inventory_name = data['inventory_name']
            inventory_category = data['inventory_category']
            inventory_desc = data['inventory_desc'] 
            inventory_merk = data['inventory_merk']
            inventory_room = data['inventory_room']
            inventory_storage = data['inventory_storage']
            inventory_rack = data['inventory_rack']
            inventory_price = data['inventory_price']
            inventory_unit = data['inventory_unit']
            inventory_vol = data['inventory_vol']
            inventory_capacity_unit = data['inventory_capacity_unit'] 
            inventory_capacity_vol = data['inventory_capacity_vol']
            is_favorite = data['is_favorite']
            created_at = datetime.utcnow()
            created_by = data['created_by']

            errors_validation = []
            inventory_name_validate = validate_data(inventory_name, 'Inventory Name', 'string', max_length=75, min_length=2, is_required=True)
            if inventory_name_validate:
                errors_validation += inventory_name_validate

            inventory_category_validate = validate_data(inventory_category, 'Inventory Category', 'string', max_length=75, is_required=True)
            if inventory_category_validate:
                errors_validation += inventory_category_validate

            inventory_desc_validate = validate_data(inventory_desc, 'Inventory Description', 'string', max_length=255, is_required=False)
            if inventory_desc_validate:
                errors_validation += inventory_desc_validate

            inventory_merk_validate = validate_data(inventory_merk, 'Inventory Merk', 'string', max_length=75, min_length=3, is_required=False)
            if inventory_merk_validate:
                errors_validation += inventory_merk_validate

            inventory_room_validate = validate_data(inventory_room, 'Inventory Room', 'string', max_length=36, is_required=True)
            if inventory_room_validate:
                errors_validation += inventory_room_validate

            inventory_storage_validate = validate_data(inventory_storage, 'Inventory Storage', 'string', max_length=36, is_required=False)
            if inventory_storage_validate:
                errors_validation += inventory_storage_validate

            inventory_rack_validate = validate_data(inventory_rack, 'Inventory Rack', 'string', max_length=36, is_required=False)
            if inventory_rack_validate:
                errors_validation += inventory_rack_validate

            inventory_price_validate = validate_data(inventory_price, 'Inventory Price', 'integer', is_required=True)
            if inventory_price_validate:
                errors_validation += inventory_price_validate

            inventory_unit_validate = validate_data(inventory_unit, 'Inventory Unit', 'string', max_length=36, is_required=True)
            if inventory_unit_validate:
                errors_validation += inventory_unit_validate

            inventory_vol_validate = validate_data(inventory_vol, 'Inventory Volume', 'integer', max_length=6, is_required=True)
            if inventory_vol_validate:
                errors_validation += inventory_vol_validate

            inventory_capacity_unit_validate = validate_data(inventory_capacity_unit, 'Inventory Capacity Unit', 'string', max_length=36, is_required=False)
            if inventory_capacity_unit_validate:
                errors_validation += inventory_capacity_unit_validate

            inventory_capacity_vol_validate = validate_data(inventory_capacity_vol, 'Inventory Capacity Volume', 'integer', max_length=6, is_required=False)
            if inventory_capacity_vol_validate:
                errors_validation += inventory_capacity_vol_validate

            query = insert(inventory).values(
                inventory_name = inventory_name,
                inventory_category = inventory_category,
                inventory_desc = inventory_desc,
                inventory_merk = inventory_merk,
                inventory_room = inventory_room,
                inventory_storage = inventory_storage,
                inventory_rack = inventory_rack,
                inventory_price = inventory_price,
                inventory_image = None,
                inventory_unit = inventory_unit,
                inventory_vol = inventory_vol,
                inventory_capacity_unit = inventory_capacity_unit,
                inventory_capacity_vol = inventory_capacity_vol,
                is_favorite = is_favorite,
                is_reminder = 0 ,
                created_at = created_at,
                created_by = created_by,
                updated_at=None,
                deleted_at=None 
            )

            # Exec
            result = session.execute(query)

            if result.rowcount > 0:
                data['id'] = id
                data['created_at'] = created_at.isoformat()

                # is_history_success = await create_history(
                #     type="Add Marker",
                #     ctx=inventory_name,
                #     user_id=created_by,
                #     session=session
                # )

                session.commit()
                return True, id
            else:
                return False, None
        # else:
        #     return JSONResponse(
        #         status_code=401, 
        #         content={
        #             "data": None,
        #             "message": "User account not found",
        #         }
        #     )
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close() 