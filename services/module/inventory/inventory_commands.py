from configs.configs import engine
from services.module.inventory.inventory_model import inventory
from sqlalchemy import select, insert, and_
from helpers.converter import convert_price_number
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from helpers.generator import get_UUID
from helpers.validator import validate_data
from services.module.history.history_command import create_history
import io
from xhtml2pdf import pisa
from helpers.generator import generate_doc_template
from services.module.dictionary.dictionary_queries import get_all_dct 

Session = sessionmaker(bind=engine)

async def post_inventory_query(data:dict):
    session = Session() 

    try: 
        # Name validation
        query_name = select(inventory.c.inventory_name).where(
            and_(
                inventory.c.inventory_name == data['inventory_name'],
                inventory.c.created_by == data['created_by']
            )
        )
        result_name = session.execute(query_name)
        check_name = result_name.first()

        if check_name is None:
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

            # Validation
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

            # Dictionary get
            dcts = await get_all_dct(session)
            dct_cat = []
            dct_room = []
            dct_unit = []

            # Dictionary validation
            for dt in dcts:
                if dt.dictionary_type == 'inventory_category':
                    dct_cat.append(dt.dictionary_name)
                elif dt.dictionary_type == 'inventory_unit':
                    dct_unit.append(dt.dictionary_name)
                elif dt.dictionary_type == 'inventory_room':
                    dct_room.append(dt.dictionary_name)

            if inventory_category not in dct_cat:
                errors_validation.append({
                    "field":'inventory_category',
                    "message":f'{inventory_category} not a valid inventory category'
                })
            if inventory_room not in dct_room:
                errors_validation.append({
                    "field":'inventory_room',
                    "message":f'{inventory_category} not a valid inventory room'
                })
            if inventory_unit not in dct_unit:
                errors_validation.append({
                    "field":'inventory_unit',
                    "message":f'{inventory_category} not a valid inventory unit'
                })


            if len(errors_validation) == 0:
                # Command builder
                id = get_UUID()
                query = insert(inventory).values(
                    id= id,
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
                result = session.execute(query)

                if result.rowcount > 0:
                    data['id'] = id
                    data['created_at'] = created_at.isoformat()

                    # History
                    await create_history(
                        type="Create",
                        ctx=inventory_name,
                        user_id=created_by,
                        session=session
                    )

                    capacity = f"{inventory_capacity_vol or '-'} {inventory_capacity_unit or '-'}"
                    if inventory_capacity_unit == 'percentage' :
                        capacity = f"{inventory_capacity_vol or '-'}%"

                    # PDF Report
                    style_template = generate_doc_template(type="style")
                    header_template = generate_doc_template(type="header")
                    footer_template = generate_doc_template(type="footer")
                    res_doc = f"""
                    <html>
                        <head>
                            {style_template}
                        </head>
                        <body>
                            {header_template}
                            <h3 style='margin:0 0 6px 0;'>Inventory : {inventory_name}</h3>
                            <p style='margin:0; font-size:14px;'>ID : {id}</p>
                            <p style='margin-top:0; font-size:14px;'>Category : {inventory_category}</p><br>
                            <p style='font-size:13px; text-align: justify;'>
                                At {created_at}, this document has been generated from the inventory called <b>{inventory_name}</b>. 
                                You can also import this document into GudangKu Apps or send it to our Telegram Bot if you wish to analyze the inventory.
                                Important to know, that this document is <b>accessible for everyone</b> by using this link. Here you can see the item in this report:
                            </p>                    
                            <table>
                                <tbody>
                                    <tr>
                                        <th>Description</th>
                                        <td>{inventory_desc or '-'}</td>
                                    </tr>
                                    <tr>
                                        <th>Merk</th>
                                        <td>{inventory_merk or '-'}</td>
                                    </tr>
                                    <tr>
                                        <th>Room</th>
                                        <td>{inventory_room}</td>
                                    </tr>
                                    <tr>
                                        <th>Storage</th>
                                        <td>{inventory_storage or '-'}</td>
                                    </tr>
                                    <tr>
                                        <th>Rack</th>
                                        <td>{inventory_rack or '-'}</td>
                                    </tr>
                                    <tr>
                                        <th>Price</th>
                                        <td>Rp. {convert_price_number(inventory_price)},00</td>
                                    </tr>
                                    <tr>
                                        <th>Unit</th>
                                        <td>{inventory_unit}</td>
                                    </tr>
                                    <tr>
                                        <th>Volume</th>
                                        <td>{inventory_vol or '-'}</td>
                                    </tr>
                                    <tr>
                                        <th>Capacity Unit</th>
                                        <td>{capacity}</td>
                                    </tr>
                                    <tr>
                                        <th>Is Favorite</th>
                                        <td>{'Yes' if is_favorite == 1 else 'No'}</td>
                                    </tr>
                                    <tr>
                                        <th>Is Reminder</th>
                                        <td>No</td>
                                    </tr>
                                </tbody>
                            </table>
                            {footer_template}
                        </body>
                    </html>
                    """

                    # File handling
                    file_bytes = io.BytesIO()
                    pisa_status = pisa.CreatePDF(res_doc, dest=file_bytes)
                    if pisa_status.err:
                        return "Error generating PDF"

                    file_bytes.seek(0)
                    file_bytes.name = f"inventory_{id}_{inventory_name}.pdf"

                    session.commit()
                    return {
                        'status' : True, 
                        'id' : id, 
                        'inventory_name': inventory_name, 
                        'extra': file_bytes
                    }
                else:
                    return {
                        'status' : False, 
                        'id' : None, 
                        'inventory_name': inventory_name, 
                        'extra': None
                    }
            else:
                errors_validation_str = 'Validation failed\n\n'
                for dt in errors_validation:
                    errors_validation_str += f"- At {dt['field']}, {dt['message']}\n"
                return {
                    'status' : False, 
                    'id' : None, 
                    'inventory_name': inventory_name, 
                    'extra': errors_validation_str
                }
        else: 
            return {
                'status' : False, 
                'id' : None, 
                'inventory_name': data['inventory_name'], 
                'extra': "\n- At inventory_name, name already been used\n"
            }
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close() 