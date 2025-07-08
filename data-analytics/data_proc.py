import pandas as pd
import polars as pl

# Converts an access log file to a data frame
def access_log_to_df(path):


    data = []

    with open(path, 'r') as f:
        i = 0
        for line in f:
            data.append(read_access_log_entry(line))

    df = pl.DataFrame(data, schema=['ip',
                              'date',
                              'time',
                              'req_type',
                              'api_call',
                              'http_return',
                              'other_code',
                              'req_url',
                              'user_agent',
                              'final_code'])
    return df

def read_access_log_entry(entry):


    # Get the IP address
    entry_list = list(entry)
    ip = ""
    i = 0
    while entry_list[i] != " ":
        ip = ip + entry_list[i]
        i += 1

    # Burn the " - - " that's in each access log
    while entry_list[i] != "[":
        i += 1

    i += 1

    # Get the date and time of the request
    date = ""
    while entry_list[i] != ":":
        date = date + entry_list[i]
        i += 1

    i += 1
    time = ""
    while entry_list[i] != "]":
        time = time + entry_list[i]
        i += 1

    # burn next 2 chars ( and ")
    while entry_list[i] != "\"":
        i += 1

    i += 1

    # Get Request type
    # GET = true, POST = false
    req_type = (entry_list[i] == 'G')

    # Read through to the API string
    while entry_list[i] != " ":
        i = i + 1

    i += 1

    # Get the API call
    api_call = ""
    while entry_list[i] != "\"":
        api_call = api_call + entry_list[i]
        i += 1

    # Skip over the quotation and space
    i += 2

    # Get the HTTP return code
    http_return = ""
    while entry_list[i] != " ":
        http_return = http_return + entry_list[i]
        i += 1

    i += 1

    # Get the other code that I have no idea what it represents but it looks important
    other_code = ""
    while entry_list[i] != " ":
        other_code = other_code + entry_list[i]
        i += 1
    # Skip over the space and quotation
    i += 2

    # Get the request url (not sure what it actually is, this is just a placeholder name)
    req_url = ""
    while entry_list[i] != "\"":
        req_url = req_url + entry_list[i]
        i += 1

    # Skip over current and next quotation
    i += 3

    # Get the user agent string
    user_agent = ""
    while entry_list[i] != "\"":
        user_agent = user_agent + entry_list[i]
        i += 1

    i += 1
    # Skip over the " **"
    while entry_list[i] == " " or entry_list[i] == "*":
        i = i + 1

    # Get the final code at the end of the entry
    final_code = ""
    while entry_list[i] != "*":
        final_code = final_code + entry_list[i]
        i += 1

    return {'ip': ip,
            'date': date,
            'time': time,
            'req_type': req_type,
            'api_call': api_call,
            'http_return': http_return,
            'other_code': other_code,
            'req_url': req_url,
            'user_agent': user_agent,
            'final_code': final_code,}

