#! /usr/bin/python3
__author__ = 'Jeff Blane '

import sqlite3  # Importing sqlite3 module
import os.path
import argparse
import pyperclip # Import for copy and paste function
import sys
import shutil


parser = argparse.ArgumentParser()
parser.add_argument('-s', '--search', dest='search', help='Search the Database for tags')
parser.add_argument('-i', '--insert', dest='ins', help='Usage: -i \"One_liner\" -t \"Related tag info\"')
parser.add_argument('-r', '--row', dest='row', help='Used to Select an entry & copy result to clip board')
parser.add_argument('-t', '--tags', dest='tags', help='Used to add searchable tags')
parser.add_argument('-l', '--list', dest='list', help='Lists all entries in Database', action='store_true')
parser.add_argument('-d', '--del', dest='delete', help='Used to delete a single entry in the Database')
parser.add_argument('-R', '--reset', dest='reset', help='Used to delete info to Database', action='store_true')
parser.add_argument('-b', '--backup', dest='backup', help='Used to make a backup of the Database', action='store_true')

args = parser.parse_args()

text_green = '\033[1;32m'
text_blue = '\033[1;34m'
text_yellow = '\033[1;33m'
text_red = '\033[1;31m'
text_gray = '\033[1;30m'
text_cyan = '\033[1;36m'
text_magenta = '\033[1;35m'
text_hblue = '\033[1;44m'
text_end = '\033[0m'

if len(sys.argv) < 2:
    print('')
    print(text_cyan + 'Click script: Notepad used to store frequently use one liners with copy and paste functionality :)' + text_end)
    print((''))
    #parser.print_usage()
    print('Please use -h for more options ')
    print('')
    sys.exit(1)

def intro():
    print('')
    print (text_cyan + 'Click script: Notepad used to store frequently use one liners with copy and paste functionality' + text_end)

def db_con():
    print('No database found: Creating new db... ')
    db_create()

def db_create():
    conn = sqlite3.connect('click_scripts.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE Scripts (
                command text,
                tags text
                )''')
    conn.commit()
    conn.close()

def db_insert():
    required_together = ('ins', 'tags')
    if not all([getattr(args, x) for x in required_together]):
        print('Cannot supply -i <insert> without -t <tag>')
        exit(1)

    conn = sqlite3.connect('click_scripts.db')
    c = conn.cursor()
    c.execute('''INSERT INTO Scripts(command, tags) VALUES(?,?)''', (args.ins, args.tags))
    conn.commit()
    conn.close()
    print('Items you just inserted')
    print(args.ins + " : " + str(args.tags))

def db_list():
    conn = sqlite3.connect('click_scripts.db')
    c = conn.cursor()
    c.execute('SELECT rowid, * FROM Scripts')
    list = c.fetchall()
    for row in list:
        print(text_green + str(row[0]) + text_end,  row[1], text_blue + row[2] + text_end)
    print('')
    print('** To select an entry please use: ' + text_cyan + 'click_scripts.py -r <row id>'+text_end + '**')
    print('')

def db_search():
    conn = sqlite3.connect('click_scripts.db')
    c = conn.cursor()
    c.execute("select rowid,* from Scripts WHERE tags LIKE ?", ('%' + args.search + '%',))
    if c.fetchone() is None:
        print('Search results empty... Please select one of the following available tags..')
        c.execute('SELECT DISTINCT tags FROM Scripts')
        for row in c:
            print(text_cyan +' tag: '+text_end + ('{0}'.format(row[0])))
    else:
        c.execute("select rowid,* from Scripts WHERE tags LIKE ?", ('%' + args.search + '%',))
        search = c.fetchall()
        for row in search:
            print (text_green + str(row[0]) + text_end, row[1], text_blue + row[2] + text_end)
            pyperclip.copy('{1}'.format(row[0], row[1], row[2]))
        print('')
        print('** To select an entry please use: ' + text_cyan + 'click_scripts.py -r <row id>' + text_end + '**')
        print('')

def row_id_search():
    conn = sqlite3.connect('click_scripts.db')
    c = conn.cursor()
    c.execute('SELECT DISTINCT rowid, * FROM Scripts WHERE rowid=:rowid', {"rowid": args.row})
    for row in c:
        print (text_magenta + 'Command copied to clipboard: '+text_end + ('{1}'.format(row[0], row[1], row[2])))
        pyperclip.copy('{1}'.format(row[0], row[1], row[2]))

def db_reset():
    check_del = input(text_red + '**ALERT** type <YES> ONLY if you are sure you want to remove the database: ' + text_end)
    if check_del == 'YES':
        os.remove('click_scripts.db')
        print('Database removed!')
    else:
        print('Database not deleted!')

def db_backup():
    print(text_red + 'WARNING : ' + text_end + 'This will over write you previous backup.db file')
    backup = input('To backup your database type YES -> : ')
    if backup == 'YES':
        shutil.copy2('click_scripts.db', 'backup.db')
        print('Database backup done!')
    else:
        print('no backup done')

def db_delete():
    conn = sqlite3.connect('click_scripts.db')
    c = conn.cursor()
    c.execute('DELETE FROM Scripts WHERE rowid=:rowid', {"rowid": args.delete})
    print("Row " + (text_red + args.delete + text_end) + " removed!")
    conn.commit()
    conn.close()


def main():
    file = 'click_scripts.db'
    intro()

    if os.path.isfile(file):
        print('')
    else:
        db_con()

    if args.search:
        db_search()

    if args.ins:
        db_insert()

    if args.list:
        db_list()

    if args.row:
        row_id_search()

    if args.reset:
        db_reset()

    if args.delete:
        db_delete()

    if args.backup:
        db_backup()

if __name__ == '__main__':
    main()

# To Do...
# Add update db function from git
# Add backup db function
