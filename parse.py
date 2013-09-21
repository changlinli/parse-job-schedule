import sys
import getopt
import xml.etree.ElementTree as ET
import colorama
import termcolor
import datetime

USEAGE = \
"""
Useage:
parse.py filename
filename: The XML file containing the company names I wish to apply for
"""

def binary_partition(input_list, predicate):
    """
    Partitions a given list based on a given boolean function and returns a list
    of the two sub-lists generated.

    Positional Arguments:
    input_list -- The list we wish to partition
    predicate -- The boolean function which we wish to use for the partition
    """
    first_partition = []
    second_partition = []
    for item in input_list:
        if predicate(item):
            first_partition.append(item)
        else:
            second_partition.append(item)
    return [first_partition, second_partition]

def gen_companies(filename):
    """
    Given an appropriate XML file containing companies I wish to apply for,
    return a partition of the companies based on their application status (i.e.
    whether I have already applied).
    """
    tree = ET.parse(filename)
    root = tree.getroot()
    companies = [child for child in root]
    companies_partition = binary_partition(companies, 
                                           lambda x: x.attrib['applied'] == "1")

    return companies_partition

def print_company_info(company, deadline = False, materials = False):
    """
    Print the required materials and deadline associated with the company.
    """
    try:
        company_position_name = company.find('position').find('name').text
    except AttributeError:
        company_position_name = ""
    print("{0} - {1}".format(company.find('name').text, company_position_name))
    if materials == True:
        try:
            materials = [element.text for element in
                         company.find('position').find('materials').findall('item')]
            print("    Requirements: {0}".format(str(materials)))
        except AttributeError:
            pass
    if deadline == True:
        try:
            deadline = company.find('position').find('deadline').text.strip()
            date_obj = str2date(deadline)
            if date_obj > datetime.datetime.now() + datetime.timedelta(days=14):
                deadline = termcolor.colored(deadline, 'green')
            elif (date_obj > datetime.datetime.now() +
                  datetime.timedelta(days=7)):
                deadline = termcolor.colored(deadline, 'blue')
            elif (date_obj > datetime.datetime.now() +
                  datetime.timedelta(days=3)):
                deadline = termcolor.colored(deadline, 'yellow')
            else:
                deadline = termcolor.colored(deadline, 'red')
            print("    Deadline: {0}".format(str(deadline)))
        except AttributeError:
            pass

def str2date(input_string):
    try:
        return datetime.datetime.strptime(input_string, "%B %d, %Y")
    except ValueError:
        pass
    try:
        return datetime.datetime.strptime(input_string, "%b %d, %Y")
    except ValueError:
        return datetime.datetime.strptime("Dec 12, 2013", "%b %d, %Y")

###############################################################################
## Main Program starts here!
###############################################################################
if __name__ == "__main__":
    colorama.init()
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "ad", ["argh"])
    except getopt.GetoptError:
        print("Oops something went wrong!")
        sys.exit(2)
    if len(args) == 0:
        print("Give me an argument!")
        print(USEAGE.strip())
        sys.exit(3)

    companies_partition = gen_companies(args[0])
    already_applied = companies_partition[0]
    not_yet_applied = companies_partition[1]
    print("Already Applied:")
    print("----------------\n")
    for company in already_applied:
        print_company_info(company)
    print("\n================\n")
    print("Not Yet Applied:")
    print("----------------\n")
    for company in not_yet_applied:
        print_company_info(company, deadline = True, materials = True)
