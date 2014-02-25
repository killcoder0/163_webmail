

file_handler = open("qq_record.txt","r")

def get_addr_provider(count):
    mail_list = []
    for i in range(count):
        line = file_handler.readline().strip()
        mail_list.append("%s@qq.com"%line)
    return mail_list