'''
Common functions for manage.py commands, sheduler
and api requests
'''

# Used by:
#  newscolector.views
#  newscolector.commands.update_database

import newscollector.source_getter as source
import newscollector.base_manager as base


def update_database():
    print('update_database placeholder fired!')
    return  # placeholder
    data = source.all()
    data.sort(key=lambda item: item['date'], reverse=True)
    base.save(data)
