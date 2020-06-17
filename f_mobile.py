def main():
    import os
    import csv
    from steam_community_market import Market, AppID
    import yagmail
    message_list = []
    parent = ((os.path.dirname(os.path.realpath(__file__))).replace("\\","/"))
    address = parent + "/skins.csv"
    text_address = parent + "/f_mobile.txt"
    skin_list = []
    
    data_types = ["GUN","SKIN NAME","GRADE","MIN","MAX","CURRENT PRICE","SALE PRICE","PREV PRICE","INCREASE"]
    list_of_lists = []
    line_count = 0
    
    #STEAM MARKET
    text_file = open(text_address,"r")
    lines = text_file.readlines()
    currency = (((lines[0].strip("CURRENCY = ")).strip(" ")).strip("\n")).upper()
    market = Market(currency)

    #OPEN CSV FILE FOR READING
    csv_file = open(address,'r')
    csv_reader = csv.reader(csv_file,delimiter=',')

    for row in csv_reader:
        if line_count == 0:
            title = row
            line_count += 1
        else:
            line_count += 1
            skin_list.append(f"{row[0]} | {row[1]} ({row[2]})")
            list_of_lists.append(row)

    #GETTING PRICES AND ADDING TO LIST
    for i in range(len(skin_list)):
        try:
            #item = "AK-47 | Redline (Field-Tested)"
            item = skin_list[i]
            x = market.get_lowest_price(item, AppID.CSGO)
            if x != None:
                list_of_lists[i][7] = list_of_lists[i][5]
                
                list_of_lists[i][8] = round((x - float(list_of_lists[i][5])),3) #INCREASE
                list_of_lists[i][5] = x #CURRENT
                if x < float(list_of_lists[i][3]):
                    message_list.append(f"{skin_list[i]} is at {currency} {x} and is below the minimum of {currency} {list_of_lists[i][3]}! \n\n")
                    print("min")
                    #LESS THAN MIN
                if x > float(list_of_lists[i][4]):
                    message_list.append(f"{skin_list[i]} is at {currency} {x} and is above the maximum of {currency} {list_of_lists[i][3]}! \n\n")
                    print("max")
                    #GREATER THAN MAX
            
            if x != None:
                sale_price = x/1.15
                list_of_lists[i][6] = round(sale_price,3)

        except:     pass
                
    #WRITING TO CSV FILE
    with open('Skins.csv','w+',newline='') as csv_write:
        csv_writer = csv.writer(csv_write,delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(data_types)
        print(data_types)
        for row in list_of_lists:
            print(row)
            csv_writer.writerow(row)

    BODY = ""
    for line in message_list:
        BODY = BODY + line
        
    receiver = "alexbissessur@gmail.com"
    body = BODY
    yag = yagmail.SMTP("baichoo04@gmail.com","delafaye6942")
    yag.send(
        to=receiver,
        subject="Some Of Your Skins Are Below/Above The Specified Threshold!",
        contents=body
    )
     
main()
