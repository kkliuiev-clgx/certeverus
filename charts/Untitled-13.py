

dict2 = {"attribs": "A,B,C" , 
        "driver": "Jordyne"}

items = []
        

attriblist = dict2['attribs'].split(',')
print(attriblist)
for attribs in attriblist:
    items.append(
        {
            "driver": dict2['driver'],
            "attribs": attribs
        }
    )
    
    
print(items)

