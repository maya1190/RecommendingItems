import numpy as np 
import math
import re
import operator

#Reading History File To Create Item Dictionary---------------------------------------------------------------------------
with open("history.txt", "r") as h:
    history = h.read().split('\n')

    #to get the first line info + assign them to variables
    info = history[0].split(' ')
    del(history[0]) #delete so that it doesnt get read later on
    customer_no = int(info[0])
    items_no = int(info[1])
    #excludes the last index of the line as not used

    transactions = [] 
    for line in history:
        transactions.append(line.strip().split(' '))

items_table = {} #item-to-item collaborative table
counter = 0
positive_entries = 0

for t in transactions:
    Item_ID = transactions[counter][1]
    counter += 1
    if Item_ID not in items_table:
        items_table[Item_ID] = customer_no * [0] #making the skeleton of the dict
    for customer in range(1, customer_no + 1):
        if int(items_table[Item_ID][customer - 1]) != 1 and int(t[0]) == customer: 
            items_table[Item_ID][customer - 1] = 1
            positive_entries += 1
#--------------------------------------------------------------------------------------------------------------------------

def query_reading():
    with open("queries.txt", "r") as q:
        query = q.readlines()
    return query

#Code to perform angle calculations
#Taken from Learning Central
#Accessed 01-04-2021
#https://learningcentral.cf.ac.uk/bbcswebdav/pid-5806988-dt-content-rid-18890998_2/courses/2021-CM1208/DocumentMatching.html
def angle_calculation(x, y): 
    norm_x = np.linalg.norm(x)
    norm_y = np.linalg.norm(y)
    cos_theta = np.dot(x, y) / (norm_x * norm_y)
    if cos_theta < 1.000001 and cos_theta > 1:
        cos_theta = 1
    theta = math.degrees(math.acos(cos_theta))
    return theta
#End of referenced code.

def angle_dictionary(): 
    angle_dict = {}
    for a in range(1, items_no + 1):
        angle_dict[a] = items_no * [0] #building a skeleton for the angle dict

    total = [] #for working out the average angle
    for i in range (1, items_no + 1):
        for j in range (1, items_no + 1):
            angle = angle_calculation(items_table[str(i)], items_table[str(j)])
            angle_dict[i][j - 1] = angle
            if i != j: 
                total.append(angle)
            
    print(f'Average angle: {np.mean(total):.2f}')
    return angle_dict

def main():
    print(f'Positive entries: {positive_entries}') 
    angle_dict = angle_dictionary() #prints out the average angle aswell
    query = query_reading()

    for i in range(len(query)):
        angles = {} #angles for all customers for the current shopping basket
        angles_chosen = [] #min_angles chosen for each item in the shopping basket
        recommend_dict = {}
        recommend = []

        shopping_cart = query[i].strip().split(' ')
        print("Shopping cart:", *shopping_cart) 
        for Item_ID in shopping_cart:
            #build a dictionary for the angles specific to the basket 
            angles[Item_ID] = angle_dict[int(Item_ID)][:] 

            for item in shopping_cart: #makes sure items in the basket don't get recommended
                angles[Item_ID][int(item) - 1] = 0

            list_angles = np.array(angles[Item_ID])
            Min_angle = np.min(list_angles[list_angles != 0]) #makes sure 0 doesn't become the min angle
            angles_chosen.append([Item_ID, Min_angle])
            chosen = angles[Item_ID][:]

            if Min_angle != 90:
                print(f'Item: {Item_ID}; match: {chosen.index(Min_angle) + 1}; angle: {Min_angle:.2f}') 
                recommend_dict[chosen.index(Min_angle) + 1] = Min_angle
            else:
                print(f'Item: {Item_ID} no match')

        sorted_recommend_dict = sorted(recommend_dict.items(), key = operator.itemgetter(1)) #orders them in increasing order
        for i in sorted_recommend_dict:
            recommend.append(i[0]) #gets the item number
        print("Recommend:", *recommend)
main()
