from pywhatkit import *

###########################
##OPENS THE OVERVIEW FILE##
###########################

with open("Overview.csv","r",encoding = "utf-8") as file:
    
    temp = file.readlines() #readfiles
    
    data = [] #init a list to store the data
    
    for element in temp:
        data.append(element.strip().split(","))
        
##############################
##EXTRACT DATA FROM OVERVIEW##
##############################

examname = data[0][0] #finds the exam name
headers = data[0][1:-1] #Removes exam name and phone number section
information = data[2:] #Isolates the data points of the candidates

maxscore = {} #creates a dictionary to store the max score

totalmarks = 0 #initialise a totalmarks variable

for i in range(1,len(data[1])-1):
    maxscore.update({headers[i-1]:data[1][i]}) #creates a dictionary of the maximum scores
    
    totalmarks = totalmarks + int(data[1][i])
    
    
########################################
##FUNCTIONS TO READ THE QUESTION FILES##
########################################


def readfile(filename): #reads and interprets question file
    with open(filename,"r") as file:
        temp = file.readlines()
        data = []
        
        for element in temp:
            data.append(element.strip().split(","))
            
    qnum = data[0][0]
    headers = data[0][1:] #remove the question number and leave the criteria
    
    resultsdict = {}
    
    for element in data[1:]:
        resultsdict.update({element[0]:None}) #Initialise a dictionary associated with names
        
        scoredict = {} #initialise a dict of the score with format {criteria: score}

        lostmark = [] #criteria where the candidate lost marks
        gotmark = [] #criteria where the candidate got marks
        
        for i in range(0,len(headers)):
        
            
            if element[i+1] == "0": #did not manage to score the mark for this
                lostmark.append(headers[i]) #add to criteria where they lost mark
                
            else:
                gotmark.append(headers[i]) #add to criteria where they gained mark
            
        
        resultsdict.update({element[0]:{"lostmark":lostmark, "gotmark":gotmark}}) #Create a nested dictionary with key names that stores where they got and lost marks
    
    return resultsdict,qnum


def appendtomessage(name,resultsdict,message,qnum): #adds necessary info to the message given to each recipient
    message += f"<h2>{qnum}</h2>"
    components = resultsdict[name] #extract info about the components scored 
    
    if not components["lostmark"]: #didnt lose marks
        message += "You didn't lose any marks in this! Good job!"
        
    elif not components["gotmark"]: #didnt gain a single mark
        message += "I'm sorry but you didn't gain any marks here :("
        
    else: 
        
        message += "<table style='border: 1px solid black;'><th style='border: 1px solid black;'>Places you scored in</th>"
        for element in components["gotmark"]: #print elements where they gained marks
            message += f"""<tr><td style='border: 1px solid black;'>{element}</td></tr>"""
            
        message += "</table><br>"
            
        message += f"""<table style='border: 1px solid black;'><th style='border: 1px solid black;'>You failed to do the following:</th>""" 
        
        for element in components["lostmark"]: #print elements where they lost marks
            message += f"""<tr><td style='border: 1px solid black;'>{element}</td></tr>"""
            
        message += "</table>"
            
    return message

questions = [] #list of questions

def addquestion(filename):
    global questions 
    
    questions.append(tuple(readfile(filename)))

############################################################
##CREATING DICTS FOR EACH QUESTION (USER INPUT REQUIRED!!)##
############################################################

#FORMAT: addquestion(<filename>). Please call the functions *in the order of the question*, if not it will appear out of order

addquestion("Q1.csv")
addquestion("Q2.csv")

#ADD MORE QUESTIONS IF NECESSARY, FOLLOW FORMAT ABOVE

###################################
##ASSEMBLING AND SENDING MESSAGE##
###################################
    
for element in information: #looking at specific entry, i.e. each person
    
    marksscored = 0 #marks scored by candidate
    resultsdict = {} #creates a new dictionary per new person
    
    name = element[0] #extract name

    email = element[len(element)-1] #extract email
    
    
    for i in range(1,len(data[1])-1): #assigns the grades to each header
        resultsdict.update({headers[i-1]:element[i]})
        marksscored += int(element[i])
    
    
    message = f"<p>Hello {name}, These are your results for {examname}:</p>"
    
    #Overview section
    
    message += """<h2>Overview</h2>
                        <br><table style='border: 1px solid black;'>
                        <tr>
                            <th style='border: 1px solid black;'>Paper</th>
                            <th style='border: 1px solid black;'>Score</th>
                            <th style='border: 1px solid black;'>Percentage</th>
                        </tr>"""
    indivscore = {}
    for (paper,score) in resultsdict.items():
        indivscore.update({paper:score}) #add to the dictoinary of scores
        
        message += f"""<tr>
                            <td style='border: 1px solid black;'>{paper}</td>
                            <td style='border: 1px solid black;'>{score}/{maxscore[paper]}</td>
                            <td style='border: 1px solid black;'>{round(int(score)/int(maxscore[paper])*100,2)}</td>
                        </tr>"""
    
    message += "</table>\n\n"
    
    message += f"<h1>Grand total: {marksscored}/{totalmarks} ({round(marksscored/totalmarks * 100,2)}%)</h1><br><br>"
    

    
    #add in results for individual questions
    
    for question in questions:
        message = appendtomessage(name,question[0],message,question[1])
        
    #send the message
    
    print(email) #for checking purposes on the sending end

    #INPUT YOUR EMAIL AND APP PASSWORD FOR THE EMAIL!
    
    send_hmail("<email>","<app password>", f"Results for {examname}",message,email)
