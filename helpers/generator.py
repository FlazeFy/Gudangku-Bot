from datetime import datetime

def generate_doc_template(type):
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
