"""A collection of function for doing my project."""

import numpy_financial as npf
import random
import string
import os

status_list = ["yes", "investment", "loan", "mortgage"]

ask_explain = "Do you want me to explain what is present value, future value, payment, required rate per year, or required time period? (yes/no) "

no_investment = ["You should start investing for your retirement.", "You need to find out how powerful the investment is.",
                 "I'm happy you're not in debt, but you should have some investments.",
                 "Let me tell you, 80% of Warren Buffett's wealth was accumulated after 50 years old by long term investment."]

ask_value_list = ["Which value do you want to know? Please specify.", "Which value can I help you find out? Please specify."]

value_list = ["present value", "future value", "payment", "required rate per year", "required time period"]

unknown_input_reply = ["I'm not sure what do you mean.", "Can you be more specific?", "If you want to end the chat, just reply 'quit'."]

explain_value_dict = { "present value" : "The amount of money you have now, or the amount you need to invest or borrow now ! \n", 
                      "future value" : "The amount of money you will get ( or want to get ) after required time period ! It could also be 0 if you want to know the payment of the loan! \n", 
                      "payment" : "The capital you want ( or need ) to invest in each year, or the amount of money you want ( or need ) to pay off your debt in each year before due ! \n", 
                      "required rate per year" : "The rate of return you need to reach your investment goal, or the interest rate you can (or need to) handle for your loan! \n If its 10%, please input 0.1 later !\n ", 
                      "required time period" : "The number of years you want to invest, or have to pay off your debt (from now to due) ! \n" } 

quit_list = ["quit", "bye"]

first_reply = "Hi, I'm Financee'. I can evaluate your investment or loan. Do you have any investment or loan ? (yes/no)"


#Create a function to check if user wants end chat, return a boolean to determine
def end_chat(input_string):
    """ end_chat checks if an input is one of the key words that can end the chat. 
    
    Parameters
    ---------
    param1 : String
        The string is either a key word to end the chat, or not a key word and continue the chat.
    
    Returns
    ------
    Return1 : Boolean
        Returning Boolean for further conditional statements. 
        If user request to end the chat, return True. Otherwise, return False.
    """
    if input_string in quit_list:
        print("Bye !")
        return True


#check if the conversation continue to next stage, or end chat
def if_continue(input_string):
    """ if_continue figures out whether or not the users have investment or loan to evaluate, or if they want to try the chatbot.
    
    Parameters
    ---------
    param1 : String
        The string indicates if further conversation is needed.
        
    Returns
    ------
    Return1 : Boolean
        Returning True if users have something to evaluate, and trigger next part of conversation.
        Returning False if users don't want to try the chat, and want to end the chat.
    """
    if input_string in status_list:
        print(ask_explain)
        return True
    else:
        print(random.choice(no_investment))
        print("Do you want to try again my service?")
        msg = input('INPUT :\t')
        if end_chat(msg):
            return False
        elif msg == "no":
            return False
        elif msg == "yes":
            print(ask_explain)
            return True
        else:
            return if_continue(msg)
    

    
# check if user need explaination for parameter
def if_explain(input_string):
    """ if_explain checks whether the user needs explaination for the terms show up in later questions.
    
    Parameters
    ---------
    param1 : String
        It specify whether the explaination is requested.
    
    Returns
    ------
    Return1 : Dictionary
        The dictionary contains all the terms be used in future questions as the key, and corresponding explaination as the value.
        
    Return2 : Boolean
        Returning Boolean to identify if user wants to end or continue the chat.
    """
    
    if "yes"== input_string:
        for key, value in explain_value_dict.items():
            print(key, " : ", value)      
        print(random.choice(ask_value_list))
        
    elif "no" == input_string:
        print(random.choice(ask_value_list))
            
    elif end_chat(input_string):
        return False
            
    # use else to prevent error message        
    else:
        print(random.choice(unknown_input_reply))
        print("Do you want to try my service again?")
        msg = input('INPUT :\t')
        
        if msg == "no" or  end_chat(msg) :
            return False
        else:
            return if_explain(msg)    

# to identify which value the user wants, and remove it from the list to ask another four value for calculation
def type_object(input_string): 
    """ type_object identify the final calculation goal, and collect needed info to dictionary from users.
    
    Parameters
    ---------
    param1 : String
        It specify which term is the final goal for value caculation.
    
    Returns
    ------
    Return1 : Dictionary
        The dictionary stores the float provided by user as value,  stores corresponding terms in value_list as key.
    """

    value_list = ["present value", "future value", "payment", "required rate per year", "required time period"]
    ask_value_reply = {}
    
    #avoiding value error, chatbot would keep asking which value is requested until a correct input
    try:
        ask_value_reply['input_string'] = input_string
        value_list.remove(input_string)  
    except ValueError:
        if end_chat(input_string):
            return False
        else:
            print(random.choice(unknown_input_reply))
            print(random.choice(ask_value_list))
            msg = input("INPUT: \t")
            
            if end_chat(msg):
                return False
            else:
                try:
                    ask_value_reply['input_string'] = msg
                    ask_value_reply = (type_object(msg))    
                except TypeError:
                    return False
                
                return ask_value_reply
        
    # start asking value needed for calculation to store in a dictionary for next stage, and also avoiding value error. 
    
    for item in value_list:
        status = True
        while status:
            value = input("What is your " + item + "?")
                
            if end_chat(value):
                    return False
            else:
                try:
                    value = float(value)
                    ask_value_reply[item] = value
                    status = False   
                except:
                    print(item+' is a wrong type of input. Please input a number with no special characters~')
             
    return ask_value_reply
            
      

# basically a caculator fuction to caculate the requested value based on info in previous dictionary
#ask_reply is the output of type_object fuction which is a dictionary
def calc_parameter (ask_reply, input_string):
    """ calc_parameter is a calculator to calculate the final goal based on ino given by users.
    
    Parameters
    ---------
    Param1 : Dictionary
        The dictionary stores the float provided by user as value,  stores corresponding terms as the key.
        
    Param2 : String
        The string is the specified goal for caculation. 
        The string implies what the dictionary would be since each value is dependent to the remaining values. 
        
    Returns
    ------
    Return1 : Float
        The final result of requested value after caculation.
    """
    user_fin_dict = ask_reply

    try:
        if(ask_reply['input_string']) == 'present value':
            output = abs(npf.pv(user_fin_dict["required rate per year"], user_fin_dict["required time period"], 0-user_fin_dict["payment"], user_fin_dict["future value"]))
        elif(ask_reply['input_string']) == "future value":
            output = abs(npf.fv(user_fin_dict["required rate per year"], user_fin_dict["required time period"], 0-user_fin_dict["payment"], 0-user_fin_dict["present value"]))
        elif(ask_reply['input_string']) == "payment":
            output = abs(npf.pmt(user_fin_dict["required rate per year"],user_fin_dict["required time period"], 0-user_fin_dict["present value"], user_fin_dict["future value"]))
        elif(ask_reply['input_string']) == "required rate per year":
            output = abs(npf.rate(user_fin_dict["required time period"], 0-user_fin_dict["payment"], 0-user_fin_dict["present value"], user_fin_dict["future value"]))
        elif(ask_reply['input_string']) == "required time period":
            output = abs(npf.nper(user_fin_dict["required rate per year"], 0-user_fin_dict["payment"], 0-user_fin_dict["present value"],user_fin_dict["future value"]))
        else:
            output = random.choice(unknown_input_reply)
        return output
    
    except KeyError:
        print("I'm dead because of you !")
        print("You should never have encountered this. What did you do?")
        return None


    
# The main function executing all minor functions to operate the chatbot
def have_a_chat ():
    """ have_a_chat is the main function to operate the chatbot.
    
    Parameters
    ---------
    None
    
    Returns
    ------
    Return1 : Float
        The numerical value was requested by user.
    """
    #Initializing chat in order to keep looping until the chat end
    chat=True
    
    # The first message send to users to begin the chat
    print(first_reply)
    
    # Keep the chatbot working until the chat is ended
    while(chat):   

        # Dividing the conversation into four parts and initialize them as True
        
        #The first part take the user's input from first reply, to see whether continue or end the chat
        first_part=True
        
        # If user chose to continue, the second part ask whether they need explaination of the terms or end the chat
        second_part = True
         
        # The third part start asking the final goal and request neccesary value from users, finally return the value they want
        third_part = True
        
        # if user end the chat, the conversation stop. Otherwise, first_part turns to False to get out of firt_part and move on
        if first_part:
            msg = input('INPUT :\t')
            if(end_chat(msg)):
                break
            if(if_continue((msg.lower()).strip())==False):
                break
            first_part = False
        
        # same logic as first part, if if_explain return False means user wants to end the chat. Otherwise second part completes.
        if second_part:
            msg = input('INPUT :\t')
            if(if_explain((msg.lower()).strip())==False):
                break
            second_part = False
            
        # In third part, stores the output from type_object to ask_reply
        # The ask_reply would either be None (end caht), or a dictionary contains value for calculation
        # If chat is not ended, the calc_parameter be executed and print the result to users
        if third_part:
            third_part = False
            #print(random.choice(ask_value_list))
            input_string = input('INPUT :\t')
            ask_reply = type_object(input_string.lower().strip())
            if ask_reply == False:
                break
            else:
                calc_value = calc_parameter(ask_reply, input_string)
                if calc_value != None:
                    print(calc_value)
                else:
                    third_part = True
                    
        if not third_part:
            chat = False
        else:
            print(first_reply)