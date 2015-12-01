def get_rating_score(rate):
    """Assigns search results score based on avg rating for class"""

    if rate <= 1:
        score = 30
    elif rate <= 2:
        score = 20
    elif rate <= 3:
        score = 10
    elif rate <= 4:
        score = 5
    elif rate <= 5:
        score = 0

    return score



def get_time_to_start(time_to_start):
    if time_to_start.days < 15:
        score = 0
    elif time_to_start.days < 30:
        score = 10
    elif time_to_start.days < 60:
        score = 15
    elif time_to_start.days < 90:
        score = 20
    elif time_to_start.days < 180:
        score = 25
    elif time_to_start.days >= 180:
        score = 30

    return score




def get_price(base_p):
    """Assigns search results score based on base price for class"""

    if base_p < 20:
        score = 0
    elif base_p < 40:
        score = 5
    elif base_p < 60:
        score = 10
    elif base_p < 80:
        score = 15
    elif base_p > 80:
        score = 20

    return score




def get_time_since_created(now, created):
    """Assigns search results score based on how soon the start date is based on now"""
    
    time_created = created - now
    print "TIME_CREATED: ", time_created.days

    if time_created.days < 30:
        score = 0
    elif time_created.days < 60:
        score = 5
    elif time_created.days >= 60:
        score = 10

    return score



def get_size(size):
    """Assigns search results score based on max_students for class"""

    if size < 20:
        size_score = 0
    elif size < 40:
        size_score = 5
    elif size > 40:
        size_score = 10
    elif size == None:
        size_score = 10

    return size_score



def get_full_status(num_enrolled, size):
    if num_enrolled == size:
        score = 20
    else:
        score = 0
    return score