# Indices of nodes
"""
    {14} . . . . {13} . . . . {12} . . . . {11} . . . . {10} . . . . {9}
    . .                                             . .
    .   .                                         .   .
    .     .                                     .     .
    .       {26}                                 {22}       .
    {15}         .                             .         {8}
    .           .                         .           .
    .             .                     .             .
    .               {25}                 {23}               .
    .                 .             .                 .
    {16}                   .         .                   {7}
    .                     .     .                     .
    .                       . .                       .
    .                        {24}                        .
    .                     .     .                     .
    {17}                   .         .                   {6}
    .                 .             .                 .
    .               {27}                 {21}               .
    .             .                     .             .
    .           .                         .           .
    {18}         .                             .         {5}
    .       {28}                                 {20}       .
    .     .                                     .     .
    .   .                                         .   .
    . .                                             . .
    {19} . . . . {0} . . . . {1} . . . . {2} . . . . {3} . . . . {4}
"""


class MapNode:

    def __init__(self, index):
        self.nexts = list()
        self.players = list()
        self.index = index

    def __str__(self):
        if self.players:
            players = '/'.join([p.name for p in self.players])
            return players
        else:
            return 'o'

    def get_next(self):
        return self.nexts[0] if len(self.nexts) else None

    @property
    def is_last(self):
        return not self.nexts


class Map:

    nodes = list()

    def __init__(self):
        for i in range(30):
            self.nodes.append(MapNode(i))
        
        for i in range(19, 0, -1):
            self.nodes[i-1].nexts.append(self.nodes[i])
        
        self.nodes[4].nexts.append(self.nodes[20])
        self.nodes[20].nexts.append(self.nodes[21])
        self.nodes[21].nexts.append(self.nodes[24])

        self.nodes[24].nexts.append(self.nodes[25])
        self.nodes[25].nexts.append(self.nodes[26])
        self.nodes[26].nexts.append(self.nodes[14])

        self.nodes[9].nexts.append(self.nodes[22])
        self.nodes[22].nexts.append(self.nodes[23])
        self.nodes[23].nexts.append(self.nodes[24])

        self.nodes[24].nexts.append(self.nodes[27])
        self.nodes[27].nexts.append(self.nodes[28])
        self.nodes[28].nexts.append(self.nodes[19])

    @property
    def head(self):
        return self.nodes[0]
