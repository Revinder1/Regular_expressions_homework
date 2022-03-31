import csv
import re


def read_csv(file_name):
    """Reading .csv file and converting data into the list"""

    with open(file_name, encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list


def reformat_phone_number(contacts_list):
    """Reformatting phone numbers into one format"""

    pattern = r'(\+7|8)[ ]?[( ]?(\d{3})[ )-]*(\d{3})[ -]?(\d{2})[- ]?(\d{2})([ ])?[( ]?(доб.)*[ ]*(\d*)[)]?'
    sub_pattern = r'\1(\2)\3-\4-\5\6\7\8'
    new_contacts_list = []
    for seq in contacts_list:
        seq_as_string = ','.join(seq)
        formatted_seq = re.sub(pattern, sub_pattern, seq_as_string)
        seq_as_list = formatted_seq.split(',')
        new_contacts_list.append(seq_as_list)
    return new_contacts_list


def reformat_full_name(contacts_list):
    """Reformatting lastnames, firstnames and surnames into one format"""

    pattern = r'^([А-ЯЁа-яё]+)(\s*)(\,?)([А-ЯЁа-яё]+)' \
              r'(\s*)(\,?)([А-ЯЁа-яё]*)(\,?)(\,?)(\,?)'
    sub_pattern = r'\1\3\10\4\6\9\7\8'
    new_contacts_list = []
    for seq in contacts_list:
        seq_as_string = ','.join(seq)
        formatted_seq = re.sub(pattern, sub_pattern, seq_as_string)
        seq_as_list = formatted_seq.split(',')
        new_contacts_list.append(seq_as_list)
    return new_contacts_list


def fix_duplicates(contacts_list):
    """Comparing lists with each other to get corrected lists without duplicates"""

    for i in contacts_list:
        for j in contacts_list:
            if i[0] == j[0] and i[1] == j[1] and i != j:
                if i[2] == '':
                    i[2] = j[2]
                if i[3] == '':
                    i[3] = j[3]
                if i[4] == '':
                    i[4] = j[4]
                if i[5] == '':
                    i[5] = j[5]
                if i[6] == '':
                    i[6] = j[6]
    new_contacts_list = []
    for seq in contacts_list:
        seq_as_string = ','.join(seq)
        formatted_seq = re.sub(',+', ',', seq_as_string)
        seq_as_list = formatted_seq.split(',')
        removing_empty_strings(seq_as_list)
        if seq_as_list not in new_contacts_list:
            new_contacts_list.append(seq_as_list)
    return new_contacts_list


def removing_empty_strings(contacts_list):
    """Removing empty strings from list"""

    for element in contacts_list:
        if element == '':
            contacts_list.remove(element)


def write_file(contacts_list):
    """Creating new .csv file, writing new contact list into it"""

    with open('phonebook.csv', 'w', newline='', encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)


if __name__ == '__main__':
    file = read_csv('phonebook_raw.csv')
    number = reformat_phone_number(file)
    name = reformat_full_name(number)
    last_fix = fix_duplicates(name)
    write_file(last_fix)
