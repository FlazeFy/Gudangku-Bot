from services.module.inventory.inventory_model import inventory
from helpers.converter import convert_price_number
from configs.configs import con
from sqlalchemy import select, desc, and_
from helpers.generator import generate_doc_template
import io
from xhtml2pdf import pisa
import csv
from datetime import datetime

async def get_all_inventory():
    # Query builder
    query = select(
        inventory.c.inventory_name, 
        inventory.c.inventory_category,
        inventory.c.inventory_merk,
        inventory.c.inventory_desc,
        inventory.c.inventory_room,
        inventory.c.inventory_storage,
        inventory.c.inventory_rack,
        inventory.c.inventory_price,
        inventory.c.inventory_unit, 
        inventory.c.inventory_vol,
        inventory.c.inventory_capacity_unit, 
        inventory.c.inventory_capacity_vol
    ).where(
        inventory.c.created_by == "2d98f524-de02-11ed-b5ea-0242ac120002"
    ).order_by(
        desc(inventory.c.is_favorite),
        desc(inventory.c.created_at)
    )

    # Exec
    result = con.execute(query)
    data = result.fetchall()

    res = f"You have {len(data)} items in your inventory.\nHere is the list:\n\n"

    for idx, dt in enumerate(data):
        capacity_element = ''
        if dt.inventory_capacity_vol:
            capacity_element = f"\nCapacity : {dt.inventory_capacity_vol} {dt.inventory_capacity_unit}"
        
        res += (
            f"{idx+1}. <b>{dt.inventory_name}</b>\n"
            f"Category / Merk : {dt.inventory_category} / {dt.inventory_merk}\n"
            f"Description :\n"
            f"{dt.inventory_desc or '<i>- No Description Provided -</i>'}\n"
            f"Room : {dt.inventory_room}\n"
            f"Storage / Rack : {dt.inventory_storage or '-'} / {dt.inventory_rack or '-'}\n"
            f"Price : Rp. {dt.inventory_price}\n"
            f"Unit : {dt.inventory_vol} {dt.inventory_unit}{capacity_element}\n\n"
        )

    return res

async def get_all_inventory_export():
    # Query builder
    query = select(inventory
    ).where(
        inventory.c.created_by == "2d98f524-de02-11ed-b5ea-0242ac120002"
    ).order_by(
        desc(inventory.c.is_favorite),
        desc(inventory.c.created_at)
    )

    # Exec
    result = con.execute(query)
    data = result.fetchall()

    if len(data) > 0:
        list_file = []
        part = 1
        output = None

        column_names = inventory.c.keys()

        for idx, dt in enumerate(data):
            if idx % 99 == 0:
                if output is not None:
                    output.seek(0)
                    res = output.getvalue() 
                    file_bytes = io.BytesIO(res.encode('utf-8'))
                    file_bytes.name = f'Pin_List_Part-{part}.csv'
                    list_file.append(file_bytes)
                    part += 1
                
                output = io.StringIO()
                writer = csv.writer(output)
                writer.writerow(column_names)

            writer.writerow([dt[i] for i in range(len(column_names))])

        if output is not None:
            output.seek(0)
            res = output.getvalue() 
            file_bytes = io.BytesIO(res.encode('utf-8'))
            file_bytes.name = f'Inventory Data_Part-{part}.csv'
            list_file.append(file_bytes)

        return list_file, True
    else:
        return "No inventory found", False

async def get_all_inventory_name():
    # Query builder
    query = select(
        inventory.c.id, 
        inventory.c.inventory_name, 
    ).where(
        inventory.c.created_by == "2d98f524-de02-11ed-b5ea-0242ac120002",
    ).order_by(
        desc(inventory.c.inventory_name)
    )

    # Exec
    result = con.execute(query)
    data = result.fetchall()

    return data

async def get_detail_inventory(id:str, type:str):
    # Query builder
    query = select(
        inventory.c.id,
        inventory.c.inventory_name,
        inventory.c.inventory_category,
        inventory.c.inventory_desc,
        inventory.c.inventory_merk,
        inventory.c.inventory_room,
        inventory.c.inventory_storage,
        inventory.c.inventory_rack,
        inventory.c.inventory_price,
        inventory.c.inventory_image,
        inventory.c.inventory_unit,
        inventory.c.inventory_vol,
        inventory.c.inventory_capacity_unit,
        inventory.c.inventory_capacity_vol,
        inventory.c.is_favorite,
        inventory.c.is_reminder,
        inventory.c.created_at,
        inventory.c.updated_at, 
    ).where(
        and_(
            inventory.c.created_by == "2d98f524-de02-11ed-b5ea-0242ac120002",
            inventory.c.id == id
        )
    )

    # Exec
    result = con.execute(query)
    data = result.first()

    if type == 'detail':
        capacity = f"{data.inventory_capacity_vol or '-'} {data.inventory_capacity_unit or '-'}"
        if data.inventory_capacity_unit == 'percentage' :
            capacity = f"{data.inventory_capacity_vol or '-'}%"

        res = (
            f"<b>{data.inventory_name}</b>\n"
            f"Category : {data.inventory_category}\n"
            f"Description : {data.inventory_desc or '-'}\n"
            f"Merk : {data.inventory_merk or '-'}\n"
            f"Room : {data.inventory_room}\n"
            f"Storage : {data.inventory_storage or '-'}\n"
            f"Rack : {data.inventory_rack or '-'}\n"
            f"Price : Rp. {convert_price_number(data.inventory_price)},00\n"
            f"Dimension : {data.inventory_vol or '-'} {data.inventory_unit}\n"
            f"Capacity : {capacity}\n"
            f"{'' if data.is_favorite != 1 else 'This item is favorited'}\n"
            f"{'' if data.is_reminder != 1 else 'This item have reminder'}\n"
            f"Props\n"
            f"Created At : {data.created_at}\n"
            f"Last Updated : {data.updated_at or '-'}\n"
        )

        style_template = generate_doc_template(type="style")
        header_template = generate_doc_template(type="header")
        footer_template = generate_doc_template(type="footer")
        img_element = ''
        if data.inventory_image:
            img_element = f"""
                <tr>
                    <th>Image</th>
                    <td style='text-align:center;'><img src='{data.inventory_image}' style='width:200px;height:200px; margin-bottom: 20px;'></td>
                </tr>
                """
            
        res_doc = f"""
        <html>
            <head>
                {style_template}
            </head>
            <body>
                {header_template}
                <h3 style='margin:0 0 6px 0;'>Inventory : {data.inventory_name}</h3>
                <p style='margin:0; font-size:14px;'>ID : {id}</p>
                <p style='margin-top:0; font-size:14px;'>Category : {data.inventory_category}</p><br>
                <p style='font-size:13px; text-align: justify;'>
                    At {data.created_at}, this document has been generated from the inventory called <b>{data.inventory_name}</b>. 
                    You can also import this document into GudangKu Apps or send it to our Telegram Bot if you wish to analyze the inventory.
                    Important to know, that this document is <b>accessible for everyone</b> by using this link. Here you can see the item in this report:
                </p>
                <table>
                    <tbody>
                        {img_element}
                        <tr>
                            <th>Description</th>
                            <td>{data.inventory_desc or '-'}</td>
                        </tr>
                        <tr>
                            <th>Merk</th>
                            <td>{data.inventory_merk or '-'}</td>
                        </tr>
                        <tr>
                            <th>Room</th>
                            <td>{data.inventory_room}</td>
                        </tr>
                        <tr>
                            <th>Storage</th>
                            <td>{data.inventory_storage or '-'}</td>
                        </tr>
                        <tr>
                            <th>Rack</th>
                            <td>{data.inventory_rack or '-'}</td>
                        </tr>
                        <tr>
                            <th>Price</th>
                            <td>Rp. {convert_price_number(data.inventory_price)},00</td>
                        </tr>
                        <tr>
                            <th>Unit</th>
                            <td>{data.inventory_unit}</td>
                        </tr>
                        <tr>
                            <th>Volume</th>
                            <td>{data.inventory_vol or '-'}</td>
                        </tr>
                        <tr>
                            <th>Capacity Unit</th>
                            <td>{capacity}</td>
                        </tr>
                        <tr>
                            <th>Is Favorite</th>
                            <td>{'Yes' if data.is_favorite == 1 else 'No'}</td>
                        </tr>
                        <tr>
                            <th>Is Reminder</th>
                            <td>{'Yes' if data.is_reminder == 1 else 'No'}</td>
                        </tr>              
                    </tbody>
                </table>
                {footer_template}
            </body>
        </html>
        """

        file_bytes = io.BytesIO()
        pisa_status = pisa.CreatePDF(res_doc, dest=file_bytes)
        if pisa_status.err:
            return "Error generating PDF"

        file_bytes.seek(0)
        file_bytes.name = f"inventory_{data.id}_{data.inventory_name}.pdf"

        return res, data.inventory_image, file_bytes
    else:
        output = io.StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow([
            'id','inventory_name', 'inventory_category', 'inventory_desc', 'inventory_merk', 'inventory_room', 'inventory_storage', 
            'inventory_rack', 'inventory_price', 'inventory_unit', 'inventory_vol', 'inventory_capacity_unit', 
            'inventory_capacity_vol', 'is_favorite'
        ])

        writer.writerow([
            data.id,
            data.inventory_name, 
            data.inventory_category,
            data.inventory_desc,
            data.inventory_merk,
            data.inventory_room,
            data.inventory_storage,
            data.inventory_rack,
            data.inventory_price,
            data.inventory_unit,
            data.inventory_vol,
            data.inventory_capacity_unit,
            data.inventory_capacity_vol,
            data.is_favorite
        ])

        output.seek(0)
        res = output.getvalue()
        now_str = datetime.now().strftime("%Y%m%d_%H%M%S")

        file_bytes = io.BytesIO(res.encode('utf-8'))
        file_bytes.name = f"update inventory at {now_str}.csv"

        res_txt = (
            f"Here's the updateable field of inventory <b>{data.inventory_name}</b> in CSV format. Send me new data of this inventory if you have finished updated.\n\n"
            f"Props\n"
            f"Created At : {data.created_at}\n"
            f"Last Updated : {data.updated_at or '-'}\n"
        )

        return res_txt, None, file_bytes