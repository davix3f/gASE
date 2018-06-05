def connect_toggles(toggles_list, toggles_dictionary, functions_dictionary):
    if len(toggles_list) != len(functions_dictionary):
        print("The length of the argument \'toggles_list\' is", len(toggles_list),\
              "while the length of the \'functions_dictionary\' argument is", len(functions_dictionary))
        return(False)
    index = 0
    while index < len(toggles_list):
        #print(toggles_dictionary[toggles_list[index]], functions_dictionary[toggles_list[index]])
        toggles_dictionary[toggles_list[index]].connect(functions_dictionary[toggles_list[index]][0],\
                                                        functions_dictionary[toggles_list[index]][1])
        index += 1


def list_epure(target_list, *args):
    try:
        for item in args:
            target_list.remove(item)
            print("Removed \'%s\'" % item)
        return(True)
    except:
        return(False)
