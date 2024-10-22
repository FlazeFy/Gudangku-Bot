import binascii
from datetime import datetime
import csv
import io
import random 

def get_UUID():
    random_bytes = random.randbytes(16)
    hex_str = binascii.hexlify(random_bytes).decode('utf-8')

    time_low = hex_str[0:8]
    time_mid = hex_str[8:12]
    time_hi_and_version = hex_str[12:16]
    clock_seq_hi_and_reserved = int(hex_str[16:18], 16) & 0x3f
    clock_seq_low = int(hex_str[18:20], 16)
    node = hex_str[20:32]

    uuid = f"{time_low}-{time_mid}-{time_hi_and_version}-{clock_seq_hi_and_reserved:02x}{clock_seq_low:02x}-{node}"
    
    return uuid

def generate_doc_template(type:str):
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")

    if(type == "footer"):
        return f"""
            <br><hr>
            <div>
                <h6 class='date-text' style='margin: 0;'>Parts of FlazenApps</h6>
                <h6 class='date-text' style='margin: 0; float:right; margin-top:-12px;'>Generated at {current_datetime} by <span style='color:#3b82f6;'>https://gudangku.leonardhors.com</span></h6>
            </div>
        """
    elif(type == "header"):
        return """
            <div style='text-align:center;'>
                <h1 style='color:#3b82f6; margin:0;'>GudangKu</h1>
                <h4 style='color:#212121; margin:0; font-style:italic;'>Smart Inventory, Easy Life</h4><br>
            </div>
            <hr>
        """
    elif(type == "style"):
        return """
            <style>
                body { font-family: Helvetica; }
                table { border-collapse: collapse; font-size:10px; width:100%; }
                td, th { border: 1px solid #dddddd; text-align: left; padding: 8px; }
                th { text-align:center; }
                .date-text { font-style:italic; font-weight:normal; color:grey; font-size:11px; }
                thead { background-color:rgba(59, 131, 246, 0.75); }
            </style>
        """

def generate_csv_template(type:str, fields_name:list):
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(fields_name)
    output.seek(0)
    res = output.getvalue()
    file_bytes = io.BytesIO(res.encode('utf-8'))
    file_bytes.name = f"{type}.csv"

    return file_bytes