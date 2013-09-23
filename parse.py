# Copyright 2013 Changlin Li
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
A simple script for parsing an XML file containing job applications and the
schedule I need to adhere to use them.

Usage:

    parse.py [-c] filename

Arguments:

    filename    The XML file containing the company names I wish to apply for

Optional Arguments:

    -c          Optional argument for color output (will highlight different
    companies depending on how close the deadlines are)

Example:

    python parse.py -c test_application.xml

"""
import sys
import getopt
import xml.etree.ElementTree as ET
import colorama
import termcolor
import datetime

USAGE = __doc__

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

def print_company_info(company,
                       deadline = False,
                       materials = False,
                       color = False):
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
            if color == True:
                date_obj = str2date(deadline)
                if (date_obj > datetime.datetime.now() +
                    datetime.timedelta(days=14)):
                    deadline = termcolor.colored(deadline, 'green')
                elif (date_obj > datetime.datetime.now() +
                      datetime.timedelta(days=7)):
                    deadline = termcolor.colored(deadline, 'blue')
                elif (date_obj > datetime.datetime.now() +
                      datetime.timedelta(days=3)):
                    deadline = termcolor.colored(deadline, 'yellow')
                else:
                    deadline = termcolor.colored(deadline, 'red')
        except AttributeError:
            deadline = "Not Given"

    print("    Deadline: {0}".format(str(deadline)))

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
        opts, args = getopt.getopt(argv, "c")
    except getopt.GetoptError:
        print("Oops something went wrong!")
        sys.exit(2)

    if len(args) == 0:
        print("Give me an argument!")
        print(USAGE.strip())
        sys.exit(3)

    color_status = False
    if opts != [] and '-c' in opts[0]:
        color_status = True

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
        print_company_info(company,
                           deadline = True,
                           materials = True,
                           color = color_status)
