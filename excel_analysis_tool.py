# Generate some matplotlib plots to illustrate the world's top 10 languages by number of speakers.
# Intro to Programming 420-SN1
import matplotlib.pyplot as plt
# Some constants / reminders about which columns map to which indices
LANGUAGE = 0
FAMILY = 1
BRANCH = 2
L1_N = 3
L2_N = 4
TOTAL_N = 5

def top_languages_data(filename):
    '''Reads the file received as a parameter, processes its contents, and returns a list of lists.
    It also returns the first line of the file, so the information
    can be displayed to the user later on.

    - Reads the first line only and returns it at the end.
    - Reread the file by skipping the first line.
    - Splits each subsequent line into a list of values.
    - Converts specific columns (from index L1_N to TOTAL_N) to integers.
    - Returns the processed data as a list of lists.

    '''
    data=[]
    fp = open(filename)
    info_line = next(fp, "").rstrip("\r\n")
    for line in fp:
        line = line.strip().split(",")    # strip off the newline, then split by commas
        for ix in range(L1_N, TOTAL_N+1): # convert our int columns to int data types
            line[ix] = int(line[ix])
        data.append(line)
    fp.close() # close file

    #Turn the info type into a sequence (list).
    uncounted_type = 0
    info_line = info_line.split(",")
    new_info_line = info_line.copy()
    for element in info_line:
        if not isinstance(data[0][info_line.index(element)], (int, float)):
            new_info_line.remove(element)
            uncounted_type +=1
    return data, new_info_line, uncounted_type

def sort_together(sort_by, follower):
    '''Sorts two parallel lists together, keeping each pair of elements matched up.

    - `sort_by` is the list that decides the order (e.g., numbers of speakers).
    - `follower` is a list of the same length whose elements go with the
      elements of `sort_by` (e.g., language names). It does not affect the
      order; it just follows along.
    - `sort_by` is sorted in ascending order, and `follower` is rearranged so
      that each element stays paired with the same `sort_by` element as before.

    **How it works:**
    1. Glue each pair together into a small list: [sort_by[i], follower[i]].
    2. Sort the list of pairs. Python compares lists element by element,
       starting with the first, so the pairs are sorted by their `sort_by`
       value and each `follower` value is carried along with it.
    3. Unglue the sorted pairs back into two separate lists.

    Returns:
    - A tuple of (`sort_by_sorted`, `follower_sorted`), both lists.

    Example:
    >>> sort_together([30, 10, 20], ["c", "a", "b"])
    ([10, 20, 30], ['a', 'b', 'c'])

    '''

    # 1. Glue each pair together
    pairs = []
    for i in range(len(sort_by)):
        pairs.append([sort_by[i], follower[i]])

    # 2. Sort the pairs (by their first element, i.e., the sort_by value)
    pairs.sort()

    # 3. Unglue the pairs back into two lists
    sort_by_sorted = []
    follower_sorted = []
    for pair in pairs:
        sort_by_sorted.append(pair[0])
        follower_sorted.append(pair[1])

    return sort_by_sorted, follower_sorted

def data_prep(data, number, total_info_type):
    """
    Function that receives a list of lists of data and returns
    the data in a dictionary that will be plotted later on.
    It also receives the first line of a file and return the information
    so that the user can later select which one to analyze.

    Parameters:
    - info_line : the first line read from the file that contains information about the data.
    - data : list of list containing information to be analyzed.
    - number : position in each sublist that contains numerical
    information to return back in an ordered manner.
    """
    registrar = {}
    x = []
    y = []
    for element in data:
        x += [element[0]]
        y += [element[total_info_type + int(number) - 1]]
    for element in x:
        registrar[element] = y[x.index(element)]
    registrar = dict(sorted(registrar.items(), key=lambda item: item[1]))
    return registrar

# Main section of code.
print("""Hello! You are trying successfully to analyze the data from an Excel
file on the number of speakers of the top 10 languages in the world. For this demo,
use the file name "top_languages.csv" to see the program's capabilities!""")
filename = input("Enter the name of the file you want to analyze: ")
print(f"""
What info would you like to analyze?
Choose from the options below.""")
i = 1
data, info_line, uncounted_type = top_languages_data(filename)
for element in info_line:
    print(f"{i} - {element}")
    i +=1
print("Pro - See all the data")
answer = input("ENTER YOUR ANSWER HERE: ")

if answer.isnumeric():
    registrar = data_prep(data, answer, uncounted_type)
    x = list(registrar.keys())
    y = list(registrar.values())
    plt.barh(x, y)
    plt.title(f"Top 10 world languages by {info_line[int(answer)-1]}")
    plt.xlabel(f"{info_line[int(answer)-1]}")
    plt.ylabel("Languages")
    plt.tight_layout()
    plt.show()

elif answer in "pro" or answer in "Pro":
    plt.subplots(2, 2, figsize=(12, 4), layout='constrained')
    for i in range(0, len(info_line)):
        plt.subplot(2,2,i+1)
        registrar = data_prep(data, i+1, uncounted_type)
        x = list(registrar.keys())
        y = list(registrar.values())
        plt.rcParams.update({'font.size': 14})
        plt.suptitle("GENERAL VIEW OF THE SPEAKERS DISTRIBUTION")
        plt.barh(x, y)
        plt.title(f"Top 10 world languages by {info_line[i]}")
        plt.xlabel(f"{info_line[i]}")
        plt.ylabel("Languages")
    plt.show()
