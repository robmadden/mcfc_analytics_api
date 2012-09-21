from django.db import connection

def run_multirow_query(query, params=None):
    """
    Run a generic query and return the results
    """
    cursor = connection.cursor()

    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    results = cursor.fetchall()
    cursor.close()
    return results

def run_singlerow_query(query, params=None):
    """
    Run a generic query and return the results
    """
    cursor = connection.cursor()

    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    results = cursor.fetchone()
    cursor.close()
    return results