"""
A module for processing SAMI files to convert them into SRT format.
"""
from bs4 import BeautifulSoup
import bleach

def SubTime(mill_time):
    """ Converts absolute timings in milliseconds (used in SAMI)
    to SRT-specific timecodes formatted as 'HH:MM:SS,mmm'.
    Takes a single argument that can be both integer and string.
    Returns a string.
    """
    mill_time = int(mill_time)
    hours = mill_time//(60*60*1000)
    minutes = ((mill_time)//(60*1000))%60
    seconds = (mill_time//1000)%60
    millis = mill_time%1000
    time_str = '{:02d}:{:02d}:{:02d},{:03d}'.format(hours, minutes,
                                                    seconds, millis)
    return time_str


def SubConverter(argument):
    """
    Parses the contents of a SAMI file, if <SAMI> tag is found.
    Returns a list of strings, that represent lines of an SRT file.
    If no <SAMI> tag is found, returns False.
    """
    soup = BeautifulSoup(argument, 'html.parser')

    # Check if there's a <SAMI> tag:
    if not soup.sami:
        return False
    else:
        prev_line_time = '00:00:00,000'
        prev_line_text = ''
        line_num = 1
        file_list = []
        for sync in soup.find_all('sync'):
            this_line_time = SubTime(sync.get('start'))
            linerepr = repr(sync)
            line_clean = bleach.clean(linerepr, tags=['br'], strip=True)
            this_line_text = line_clean.replace('<br>', '\n')
            if this_line_text.endswith('\n'):
                this_line_text = this_line_text[:-1]
            # this_line_text = sync.get_text(separator='\n')
            if prev_line_text != '':
                file_list.append(str(line_num))
                file_list.append(prev_line_time + ' --> ' + this_line_time)
                file_list.extend(prev_line_text.split('\n'))
                file_list.append('')
                line_num += 1
            prev_line_time = this_line_time
            prev_line_text = this_line_text
        return file_list


if __name__ == '__main__':
    li = SubConverter(open(r'D:\Translate\Travel Man\subs\s4\4 4187820.txt', 'r').read())
    li_ind = li.index('442')
    print(li[li_ind])
    print(li[li_ind + 1])
    print(li[li_ind + 2])
    print(li[li_ind + 3])
    print(li[li_ind + 4])
    print(li[li_ind + 5])
    print(li[li_ind + 6])
    print(li[li_ind + 7])
