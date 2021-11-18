
def time(seconds, granularity=2, limit='weeks',language='english'):
    result = []

    if limit.lower() in ['weeks','w','wochen']:
        intervals = (('weeks', 604800),('days', 86400),('hours', 3600),('minutes', 60),('seconds', 1),)
    if limit.lower() in ['days','d','tage']:
        intervals = (('days', 86400),('hours', 3600),('minutes', 60),('seconds', 1),)
    if limit.lower() in ['hours','h','stunden']:
        intervals = (('hours', 3600),('minutes', 60),('seconds', 1),)
    if limit.lower() in ['minutes','m','minuten']:
        intervals = (('minutes', 60),('seconds', 1),)
    if limit.lower() in ['seconds','s','sekunden']:
        intervals = (('seconds', 1),)

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])


print(time(seconds=21344312, granularity=2, limit='h', language='en'))