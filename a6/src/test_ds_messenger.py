import ds_messenger as dsm
import ds_protocol as dsp

profile_filename = r'C:\Users\Christopher Cyr\Documents\School\First Year\Winter\ICS 32\a6\Chris.dsu'
current_profile = dsm.NaClProfile()
current_profile.load_profile(profile_filename)

post = current_profile.get_posts()[-1]
messenger = dsm.DirectMessenger(current_profile.dsuserver, current_profile.username, current_profile.password)
messenger.token, messenger.sock = dsp.join(messenger.port, messenger.dsuserver, messenger.username, messenger.password)
responses = messenger.retrieve_all()
for i in responses:
    for j in current_profile.get_posts():
        if str(i['from']) == str(j.get_recipient()):
            print(str(j.get_entry()) + f'\n{i["from"]}: ' + str(i['message']))
