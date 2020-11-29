
import pandas as pd


def airport_selector(n_total):
    
    '''
    # =============================================================================
    # First the database is loaded and cleaned up.
    # =============================================================================
    '''
    airports_df = pd.read_csv("formation_flying/airport_locations/airport_database.txt")
    #from https://openflights.org/data.html

    airports_df.columns = ['index', 'airport', 'city', 'country', 'IATA', 'ICAO', 'y', 'x', 'altitude', 'timezone', 'DST', 'tz database', 'type', 'source'  ] 
    
    airports_df = airports_df.drop([ 'index', 'airport', 'city', 'country', 'IATA', 
                                    'ICAO', 'altitude', 'timezone', 'DST',
                                    'tz database', 'type', 'source' ], axis=1)
    
    '''
    # =============================================================================
    # Below, the x and y coordinate columns are normalized.
    # =============================================================================
    '''
    cols_to_norm = ['x', 'y']
    airports_df[cols_to_norm] = airports_df[cols_to_norm].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
    
    '''
    # =============================================================================
    # Below, a random sample is taken from the database.
    # =============================================================================
    '''
    airports_df_selection = airports_df.sample(n_total)

    '''
    # =============================================================================
    # Below, the complete list of airports and the selected airports are plotted.
    # When using the batchrunner, it is wise to comment this out!!!
    # =============================================================================
    '''  
    #all airports
    airports_df.plot(x='x', y='y', style='o')

    
    #randomly selected airports
    airports_df_selection.plot(x='x', y='y', style='o')
    
    return airports_df_selection








