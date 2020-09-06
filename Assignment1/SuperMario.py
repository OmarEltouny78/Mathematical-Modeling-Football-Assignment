#Make a shot map and a pass map using Statsbomb data
#Set match id in match_id_required.

#Function to draw the pitch
import matplotlib.pyplot as plt
import numpy as np

#Size of the pitch in yards (!!!)
pitchLengthX=120
pitchWidthY=80

#ID for England vs Sweden Womens World Cup
match_id_required = 8656
home_team_required ="Croatia"
away_team_required ="England"

# Load in the data
# I took this from https://znstrider.github.io/2018-11-11-Getting-Started-with-StatsBomb-Data/
file_name=str(match_id_required)+'.json'

#Load in all match events 
import json
with open('Statsbomb/data/events/'+file_name) as data_file:
    #print (mypath+'events/'+file)
    data = json.load(data_file)

#get the nested structure into a dataframe 
#store the dataframe in a dictionary with the match id as key (remove '.json' from string)
from pandas.io.json import json_normalize
df = json_normalize(data, sep = "_").assign(match_id = file_name[:-5])

#A dataframe of shots
shots = df.loc[df['type_name'] == 'Shot'].set_index('id')
    
#Draw the pitch
from FCPython import createPitch
(fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','gray')

#Plot the shots
for i,shot in shots.iterrows():
    x=shot['location'][0]
    y=shot['location'][1]
    
    goal=shot['shot_outcome_name']=='Goal'
    team_name=shot['team_name']
    
    circleSize=2
    #circleSize=np.sqrt(shot['shot_statsbomb_xg']*15)

    if (team_name==home_team_required):
        if goal:
            shotCircle=plt.Circle((x,pitchWidthY-y),circleSize,color="red")
            plt.text((x+1),pitchWidthY-y+1,shot['player_name']) 
        else:
            shotCircle=plt.Circle((x,pitchWidthY-y),circleSize,color="red")     
            shotCircle.set_alpha(.2)
    elif (team_name==away_team_required):
        if goal:
            shotCircle=plt.Circle((pitchLengthX-x,y),circleSize,color="blue") 
            plt.text((pitchLengthX-x+1),y+1,shot['player_name']) 
        else:
            shotCircle=plt.Circle((pitchLengthX-x,y),circleSize,color="blue")      
            shotCircle.set_alpha(.2)
    ax.add_patch(shotCircle)
    
    
plt.text(5,75,away_team_required + ' shots') 
plt.text(80,75,home_team_required + ' shots') 
     
fig.set_size_inches(10, 7)
fig.savefig('Output/shots.pdf', dpi=100) 
plt.show()

passes=df.loc[df['type_name']=='Pass'].set_index('id')
(fig,ax)=createPitch(pitchLengthX,pitchWidthY,'yards','gray')
for i,thepass in passes.iterrows():
    if thepass['player_name']=='Mario Mandžukić':
        x=thepass['location'][0]
        y=thepass['location'][1]
        passCircle=plt.Circle((x,pitchWidthY-y),2,color='red')
        passCircle.set_alpha(.5)
        ax.add_patch(passCircle)
        dx=thepass['pass_end_location'][0]-x
        dy=thepass['pass_end_location'][1]-y
        passArrow=plt.Arrow(x,pitchWidthY-y, dx, -dy, width=5,color='red')
        ax.add_patch(passArrow)
plt.text(5,75,home_team_required) 
plt.text(80,75,away_team_required) 
fig.set_size_inches(10,7)
fig.savefig('Output/passes.png',dpi=100)
plt.show()
pressures=df.loc[df['type_name']=='Pressure'].set_index('id')
carries=df.loc[df['type_name']=='Carry'].set_index('id')
(fig,ax)=createPitch(pitchLengthX,pitchWidthY,'yards','gray')
for i,thepress in pressures.iterrows():
    if thepress['player_name']=='Mario Mandžukić':
        x=thepress['location'][0]
        y=thepress['location'][1]
        pressCircle=plt.Circle((x,pitchWidthY-y),2,color='red')
        pressCircle.set_alpha(.5)
        ax.add_patch(pressCircle)
plt.text(5,75,home_team_required) 
plt.text(80,75,away_team_required) 
fig.set_size_inches(10,7)
fig.savefig('Output/Press.png',dpi=100)
plt.show()
(fig,ax)=createPitch(pitchLengthX,pitchWidthY,'yards','gray')
for i,thecarr in carries.iterrows():
            if thecarr['player_name']=='Mario Mandžukić':
                x=thecarr['location'][0]
                y=thecarr['location'][1]
                carrCircle=plt.Circle((x,pitchWidthY-y),2,color='red')
                carrCircle.set_alpha(.5)
                ax.add_patch(carrCircle)
                dx=thecarr['carry_end_location'][0]-x
                dy=thecarr['carry_end_location'][1]-y
                carrArrow=plt.Arrow(x,pitchWidthY-y, dx, dy, width=5,color='red')
                ax.add_patch(carrArrow)
plt.text(5,75,home_team_required) 
plt.text(80,75,away_team_required) 
fig.set_size_inches(10,7)
fig.savefig('Output/Carry.png',dpi=100)
plt.show()
                