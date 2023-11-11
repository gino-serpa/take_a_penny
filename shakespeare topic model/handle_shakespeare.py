from pathlib import Path


def get_opus(data_path=None):
    '''
    Returns the lines form the complete works 
    of Shakespeare according to the Gutemberg Project
    '''
    if data_path==None:
        data_path = Path("")/'data'
        data_path = data_path/'complete works.txt'


    if not data_path.exists():
        print(str(data_path), ' does not exists')

    f = open(data_path,'r')
    opus = f.readlines()
    opus = [item.strip('\n') for 
                      item in opus]
    return opus


def get_begin_end_table(opus):

    # get line with content header
    for idx, line in enumerate(opus):
        if 'Contents'==line.strip(' '):
            content_line = idx
            break
    #print('Content: ', opus[content_line], content_line)
    
    # Get first content item line
    # Skip  blanks
    first_work_idx=content_line+1
    #print('first_work_idx', first_work_idx)
    while opus[first_work_idx]=='':
        first_work_idx+=1
    #print('First Work: ', opus[first_work_idx])


    end_pointer_idx=first_work_idx+1
    while opus[end_pointer_idx]!='':
        end_pointer_idx+=1
    end_pointer_idx+= -1

    return first_work_idx, end_pointer_idx


def get_works_dict():
    
    # Define Dictionary empty
    works_dict=dict()
    
    opus = get_opus()
    end_works_line = '*** END OF THE PROJECT '+\
                     'GUTENBERG EBOOK THE COMPLETE WORKS'+\
                     ' OF WILLIAM SHAKESPEARE ***'
    # find last works line number
    for idx, line in enumerate(opus):
        if end_works_line in line:
            opus=opus[:idx]
            break
            

    first_work, last_work = get_begin_end_table(opus)
    
    # Get the list of works 
    works_list = opus[first_work:last_work+1]
    works_list = [item.strip(' ')for item in works_list]

    for item in works_list:
        for idx,line in enumerate(opus):
            if line==item:
                works_dict[item]={'line':idx}
                #print(item, line, idx)
                break
    
    # Reverse the work list
    works_list=works_list[::-1]
    for work in works_list:
        work_init_line = works_dict[work]['line']
        text = opus[work_init_line:]
        works_dict[work]['text']=text
        opus = opus[:work_init_line]
    
    return works_dict


def make_corpus_sonnets():
    '''
    Returns a dict d

    d[sonnet number]= Single string with all the lines
    concatenated (added a space between lines)

    '''
    # Get all the works as coolected from the 
    # Gutemberg Project
    works_dict = get_works_dict()
    
    # From all the works select the sonnets
    # 'text' returns the lines from the GP file that 
    #correspond to the sonnets
    the_sonnets = works_dict['THE SONNETS']['text']


    # Get rid of empty lines and heading and trailing blanks
    # Also gets rid of the "THE END" at the end
    the_sonnets = [item.strip(' ') for item in the_sonnets \
                   if item!=''][:-1]


    # sonnet line tells us where each sonnet starts
    sonnet_line = dict()
    for idx,line in enumerate(the_sonnets):
        if line in [str(i) for i in range(1,155)]:
            sonnet_line[line]=idx

    # The reverse order is just to keep on cutting of 
    # the tails (it works)
    sonnets_dict = dict()
    for i in range(154,0,-1):
        sonnet_idx = sonnet_line[str(i)]
        sonnets_dict[i] = the_sonnets[sonnet_idx+1:]

        # This makes a doc of each sonnet. The
        # doc just a single long string 
        doc = ' '.join(sonnets_dict[i])

        sonnets_dict[i] = doc

        # Delete the tail
        the_sonnets=the_sonnets[:sonnet_idx]

    return sonnets_dict