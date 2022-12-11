import sqlite3


def _execute(self, query, *values, **kwargs):
    with sqlite3.connect(self.url) as connection:
        cursor = connection.cursor()
            
        cursor.execute(query, values)
            
        connection.commit()
            
        if kwargs.get('fetch'):
            fetch = kwargs.get('fetch')
                
            result = getattr(cursor, 'fetch'+fetch)()
            
            return result
            
            
        return None
