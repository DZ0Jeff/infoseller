

def find_tag(tag, html, error_msg='Não localizado...'):
    try:
        return html.find(tag, first=True).text
    
    except:
        return error_msg
    