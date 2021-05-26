import pprint
import logging
import os
import time
log_file_path = os.path.join(os.getcwd(),'stackerror.log')
logging.basicConfig(filename=log_file_path, level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)
STATUS_TYPE_LIST = ['P','M','C','T']
STATUS_EVENT_TYPE = "S"
REQUEST_EVENT_TYPE = "R"


def input_dict_validation(input_dict_list):
    """
    Validate input individual dict in a list .
  
   
  
    Parameters:
    input_dict_list (list): Input list of dicts
  
    Returns:
    bool: if valid returns True nor False
  
    """
    for i in input_dict_list:
        event_s = {
            "event_type":str,
            "status_type":str,
            "retry_count":int,
            }
        event_r = {
            "event_type":str,
           
            "retry_count":int,
            }
        if type(i) != type(event_s):
            print("Invalid Type must only be dictionary")
            return False
        if event_s.keys()!= i.keys() and event_r.keys() != i.keys():
            print("invalid Dictionary Found")
            return False
        if type(i["retry_count"]) != int:
                print("Retry count must be int")
                return False
        if event_s.keys() == i.keys():
            if i["event_type"] != STATUS_EVENT_TYPE:
                print("Invalid event type for status")
                return False
            if len(i) !=3:
                print("Invalid Lenght of Status Event")
                return False
            if i['status_type'] not in STATUS_TYPE_LIST:
                print("Invalid status type should be one of 'P','M','C','T'")
                return False
        
        if event_r.keys() == i.keys():
            if i["event_type"] != REQUEST_EVENT_TYPE:
                print("Invalid event type for request")
                return False
    return True
            

        
def input_validation_list(input_dict_list):
    """
    Validate input individual list and then dict .
  
   
  
    Parameters:
    input_dict_list (list): Input list of dicts
  
    Returns:
    bool: if valid returns True nor False
  
    """
    if type(input_dict_list) != list or input_dict_list == []:
            print("Invalid Input Please Provide List with only Dictionary values")
            return False
    
    return input_dict_validation(input_dict_list)
class Stack :
    '''Stack class consists of required methods to perform operations'''

    def __init__(self):
       
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self,item):
        self.items.append(item)

    def pop(self):
        if self.items != []:
            pop_data = self.items[-1]
            self.items.pop()
            return pop_data
        else:
            
            return False
    
    def display_list(self):
        print(self.items)
        return self.items

   
    
    def get_last_element_request(self):
        if len(self.items) >= 2:
            return self.items[-1]
        elif len(self.items) == 1:
            return self.items[0]

        else:
            print(self.items)
            return False
        

    def size(self):
        return len(self.items)
    
def main(input_dict_list):
    """
    main function to execute stacks operations.
  
    Extended description of function.
  
    Parameters:
    input_dict_list (int): Input list of dicts
  
    """
    if input_validation_list(input_dict_list):
        stored_status_type_list = []
        print("#" * 120)
        print("[+] Create/Initialized the required Queue")
         
        s=Stack()
        print("[+] Done")
        print("#" * 120)
        print("#" * 120)
        print("[+] Now Create and Push() each of event packets (given below) to the queue in the same sequence as listed")
        for data in input_dict_list:
            print(f"[+] Create and Pushing {data} in given sequence")

            s.push(data)
            pprint.pprint(f"[+] {data} Done")
            pprint.pprint(s.display_list())
        print("[+] All Done")
        print("#" * 120)
        print("#" * 120)
        while(not s.is_empty()):
            print("#" * 120)
            pop_data = s.pop()
            print("#" * 120)
            if pop_data:
                print("[+] Checking For event type")
                if pop_data['event_type'].upper() == "S":

                    print("[+] event type 'Status' found")
                    print("[+] Storing it's Status Type Value.....")
                    stored_status_type_list.append(pop_data['status_type'])
                    print(stored_status_type_list[-1])
                    print("[+] Done")
                    print("#" * 120)
                    print("#" * 120)
                    print("[+] Now Displaying it's content in Format EventType,Event status,Retry count")
                    print(f"[+] EventStatus:{pop_data['event_type']},{pop_data['status_type']},{pop_data['retry_count']}" )
                    print("[+] Done")
                    print("#" * 120)
                    print("#" * 120)
                    print("[+] Checking for C or T status type")
                    if pop_data['status_type'].upper() == "C" or pop_data['status_type'].upper() == "T":
                        print(f"[+] {pop_data['status_type']} Found")
                        print("#" * 120)
                        print("[+] Checking For Recycle Count")
                        if pop_data['retry_count'] < 2:
                            print("#" * 120)
                            print(f"[+] Retry count {pop_data['retry_count']} Found which is < 2")
                            print("[+] Incrementing Retry count by 1")
                            pop_data['retry_count'] += 1
                            print("[+] Pushing back to queue again")
                            s.push(pop_data)
                            pprint.pprint(s.display_list())
                            print("[+] Done")
                            print("#" * 120)
                        else:
                             print(f"[+] Retry count {pop_data['retry_count']} Found ")
                    else:
                         print(f"[+] {pop_data['status_type']} Found")
                    print("#" * 120)
                elif pop_data['event_type'].upper() == "R":
                    print("[+] event type 'Request' found")
                    last_el_data = s.get_last_element_request()
                    if last_el_data:
                        if last_el_data['event_type'].upper() == "S":
                            if last_el_data['status_type'].upper() == "C" or last_el_data['status_type'].upper() == "T":
                                print(f"[+] Status Type {last_el_data['status_type'].upper()} found")
                                print("[+] Now Displaying it's content in Format EventType,Event status,Retry count")
                                print(f"[+] EventRequest:{pop_data['event_type'].upper()},{pop_data['retry_count'].upper()}")
                                print("[+] Done")
                                print("#" * 120)
                            
                            else:
                               
                                if pop_data['retry_count'] < 2:#assumptions taken considering same as upper retry count limit check to avoid infinite loop
                                    print("[+] Incrementing Retry count by 1")
                                    pop_data['retry_count'] += 1
                                    print("[+] Pushing Back to Queue Again")
                                    s.push(pop_data)
                                    pprint.pprint(s.display_list())
                                    print("[+] Done")
                                    print("#" * 120)
                                else:
                                     print("[+] Max Retry Exceeded")
                   


            print("#" * 120)
            print("[+]Continuing The process until Queue is Empty") 
            print("#" * 120)


        print("#" * 120)
        print("[+] empty Array",s.is_empty(),s.display_list()) 
        print("#" * 120)
        print("[+] done")
    else:
        print("Invalid Input")
## Sample inputs
if __name__ == '__main__':
        """input_dict can also be loaded from json using file open and json library"""
#         input list of dicts
        input_dict_list = [
    
                            {
                            "event_type":"S",
                            "status_type":"P",
                            "retry_count":0,
                            },
                            {
                            "event_type":"R",

                            "retry_count":0,
                            },
            
                            {
                            "event_type":"S",
                            "status_type":"M",
                            "retry_count":0,
                            },
                            {
                            "event_type":"S",
                            "status_type":"P",
                            "retry_count":0,
                            },
                            {
                            "event_type":"S",
                            "status_type":"T",
                            "retry_count":0,
                            },
                            {
                            "event_type":"S",
                            "status_type":"P",
                            "retry_count":0,
                            },
                            {
                            "event_type":"S",
                            "status_type":"C",
                            "retry_count":0,
                            },
                            {
                            "event_type":"S",
                            "status_type":"M",
                            "retry_count":0,
                            },



                ]
      
        start_time = time.time()
       
       
        try:
#             Running main function
            main(input_dict_list)
        except Exception as e:
#             logging error
            print(e,f"loook in logging file at {log_file_path}")
            logger.error(e)
            
     
        print("#" * 120)
        print("Exiting")
        print("#" * 120)
        print("--- %s seconds ---" % (time.time() - start_time))
#         kernel died due to exit() system exit
        exit()

   
