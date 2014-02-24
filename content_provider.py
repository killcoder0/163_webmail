import content_gen


def get_new_mail_content(type):
    subject = content_gen.create_subject()
    html = content_gen.create_body(subject)
#    html = u"<div>你个死变态，烦死了</div>"
    return (subject,html)


def main():
    for i in range(0,3):
        title,content = get_new_mail_content("nighteyes.games.takeoff")
        print "*********************************"
        print title,"\n\n"
        print content

if __name__ == "__main__":
    main()
    raw_input("press")
