class Template:

    template = """
    {14} . . . . {13} . . . . {12} . . . . {11} . . . . {10} . . . . {9}       Finished: {29}
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

    def print_environ(self, map, users):
        print(self.template.format(*map.nodes))
        for user in users:
            print(f'{user}: {", ".join([str(p) for p in user.players if p.node is None])}')


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