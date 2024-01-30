
import os

# This function reads the menu file and outputs a dictionary containing the menu as well as the parsed categories
def readDescriptions(dataFolder, file):
    filename = os.path.join(dataFolder, file)
    dictMenu = {}
    allCategories = []
    with open(filename) as f:
        lines = f.readlines()
        category = ""
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if ',' not in line:
                category = line
                allCategories.append(category)
            else:
                itemid, itemname, price = line.split(',')
                if category not in dictMenu:
                    dictMenu[category] = []
                dictMenu[category].append((itemid, itemname, price))
    return dictMenu, allCategories


# Reads the order file and creates a dictionary "dictCounts" that holds the items ordered as well as their frequency
def summaryFromFiles(dataFolderName, prefix):
    dictCounts = {}
    for filename in os.listdir(dataFolderName):
        if not filename.startswith(prefix):
            continue
        filepath = os.path.join(dataFolderName, filename)
        file = None
        try:
            file = open(filepath, 'r')
            for line in file:
                itemid, quantity = line.split()
                quantity = int(quantity)
                if itemid.lower() in dictCounts:
                    dictCounts[itemid.lower()] += quantity
                else:
                    dictCounts[itemid.lower()] = quantity
        finally:
            if file:
                file.close()
    return dictCounts



# Function sorts the keys in reverse order and reorders the list so the DictOrders outputs (int value, keyname)
def dictToOrderedReversedTuples(dictCounts):
    dictOrders = []
    ordered_dict = []
    for key, value in dictCounts.items():
        dictOrders.append((value, key))

    dictOrders.sort(reverse=True)

    for value, key in dictOrders:
        ordered_dict.append((key, value))
    return dictOrders


# This file makes a dictionary of dictionaries where the key for the new dict is the itemID entry from the Dictmenu dict

def splitDictMenu(dictMenu):
    categoryDicts = {}
    for category in dictMenu.keys():
        categoryDicts[category] = {}

    # split the menu items into the appropriate category dictionaries
    for category, itemList in dictMenu.items():
        for item in itemList:
            itemId = item[0]
            itemInfo = item[1:]
            categoryDicts[category][itemId] = itemInfo

    return categoryDicts

# This function takes the user inputted categories and returns the 3 most popular orders for each catagory
def printTop3(dictMenu, dictOrders, user_categories):
    for category in user_categories:
        print(f"--------------------  {category}   --------------------")
        i = 0
        category = category.strip()
        categoryDict = splitDictMenu(dictMenu)
        singledict = categoryDict[category]
        # By this point the category has already been handled and we can sort singledict by the key of ItemID, which is also stored in dictOrders
        for num, key in dictOrders:
            try:
                name, price = singledict[key]
                price = float(price)
                formatted_price = "{:.2f}".format(price)
                formatted_string = ("{:<22}{:>8}".format(name.strip('"'), formatted_price))
                print("          ", formatted_string)
                i += 1
                if i >= 3:
                    break
            except KeyError:
                continue
    print()


# Define function main() to call the other functions and print the output.
def main():
    # Ask the user to enter a folder name and the categories they want.
    dataFolderName = input("Enter a folder name (default is 'data'): ") or 'data'
    dictMenu, allCategories = readDescriptions(dataFolderName, 'menuitems.txt')
    # Prints all categories in the menu
    print("Categories found in menu:")
    for category in allCategories:
        print(f"  {category}")

    # Asks for user input for top-3 menu categories, validates that information against the all categories list
    user_categories = input("Please enter categories you'd like to include in the Top-3 menu, separated with commas: ").split(",")
    invalid_categories = []
    valid_categories = []
    for category in user_categories:
        category = category.strip()
        if allCategories.count(category) > 0:
            valid_categories.append(category)
        else:
            invalid_categories.append(category)

    # Call other functions to create dictionaries
    dictCounts = summaryFromFiles(dataFolderName, 'ord')
    dictOrders = dictToOrderedReversedTuples(dictCounts)

    printTop3(dictMenu,dictOrders, valid_categories)
    # Printing invalid categories and all categories if an invalid category was inputted
    if invalid_categories.count() > 0:
        print("We omitted the following categories you requested, because they are not on the menu:")
        for category in invalid_categories:
            print(" ", category)
        print("The categories on the menu are:")
        for category in allCategories:
            print(" ", category)

main()