import datetime

# The dates for every major patch, so that we can potentially combine all jcg results from a
# particular patch
SRinitial = datetime.datetime(2019,3,27)
SRmini = datetime.datetime(2019,5,20)
RoGinitial = datetime.datetime(2019,6,26)
RoGVNerf = datetime.datetime(2019,7,10)
RoGBuffs = datetime.datetime(2019,7,29)
RoGmini = datetime.datetime(2019,8,22)
VRinitial = datetime.datetime(2019,9,25)
VRNerf = datetime.datetime(2019,10,29)
UCinitial = datetime.datetime(2019,12,28)
Now = datetime.datetime(2020,2,2)

# A list of the dates that each patch went live along with a descriptive name
dates = [[SRinitial, "Steel Rebellion Initial"],
        [SRmini, "Steel Rebellion mini"],
        [RoGinitial, "Return of Greatness initial"],
        [RoGVNerf, "RoG post-venge nerf"],
        [RoGBuffs, "RoG post-buffs"],
        [RoGmini, "RoG mini"],
        [VRinitial, "VR initial"],
        [VRNerf, "VR post-nerf"],
        [UCinitial, "UC initial"],
        [Now, "Now"]
        ]

