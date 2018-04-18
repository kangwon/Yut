template = """
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

    nexts = list()
    players = list()
    score = 0

    def __str__(self):
        return '+' if self.players else 'o'


class Map:

    nodes = list()

    def __init__(self):
        for i in range(29):
            self.nodes.append(MapNode())
        
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

    def __str__(self):
        return template.format(*self.nodes)


"""
o . . . . o . . . . o . . . . o . . . . o . . . . o
. .                                             . .
.   .                                         .   .
.     .                                     .     .
.       o                                 o       .
o         .                             .         o
.           .                         .           .
.             .                     .             .
.               o                 o               .
.                 .             .                 .
o                   .         .                   o
.                     .     .                     .
.                       . .                       .
.                        o                        .
.                     .     .                     .
o                   .         .                   o
.                 .             .                 .
.               o                 o               .
.             .                     .             .
.           .                         .           .
o         .                             .         o
.       o                                 o       .
.     .                                     .     .
.   .                                         .   .
. .                                             . .
o . . . . o . . . . o . . . . o . . . . o . . . . o
"""