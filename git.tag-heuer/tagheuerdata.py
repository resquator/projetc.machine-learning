"""
This library specific to golf data extracted from the Tag Heuer App.
The library creates a pandas dataframe and gives some statistical and
analyticals KPIs.

"""

from datetime import datetime
import json
from pandas.io.json import json_normalize
from collections import OrderedDict
import pandas as pd
import numpy as np

class TagHeuerData:
    def __init__(self, filename = None, player = None, courses = None):

        """
        Initialize the collection with a user.json file extracted from Tag Heuer App.
        
        Parameter:
        - filename: str, location of the source file
        - player: str, email of the player to filter on one player
        - courses: dataframe, a df which contains courses definition
        
        """
        
        self.holes_played = None
        
        
        with open(filename) as data_file:
            data = json.load(data_file, object_pairs_hook=OrderedDict)
        
        
        """
        Extract scorecards from data
        
        """
        rounds=pd.json_normalize(data['rounds'])
        self.rounds = rounds
        scorecards=rounds['scorecard.players']
        sc=scorecards
        df = pd.DataFrame()
        for i in range(0,int(sc.size)):
            one = sc[i]            
            temp=pd.json_normalize(one, errors='ignore')
            score=pd.json_normalize(temp.scores[0]).sort_values('holeNumber')
            rp=pd.json_normalize(one, errors='ignore')

            for idx, r in score.iterrows():
                score['rounddate']=datetime.fromtimestamp(r.date).strftime('%Y-%m-%d')
            
            score['golfCourse']=rounds.iloc[i,0]   
            score['firstName']=rp['roundPlayer.firstName'][0]
            score['lastName']=rp['roundPlayer.lastName'][0]
            score['email']=rp['roundPlayer.email'][0]
            df=pd.concat([df,score])
            df=df.drop('date',axis=1)

        df=df.reset_index(drop=True)

        self.holes_played = df
        
 