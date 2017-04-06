#!/usr/bin/python2

maze_ascii = """
+-+-+-+-+-+-+-+-+-+-+
    |         |     |
+-+ + +-+-+-+ + +-+-+
| |     |       |   |
+ +-+-+ + +-+-+-+ + +
|     | |   |     | |
+ +-+-+ + + + +-+-+ +
|       | | | |   | |
+-+-+-+-+ + + + +-+ +
|   |     |   | |   |
+ +-+ + +-+-+ + + +-+
|   | | |   | |   | |
+-+ + +-+ +-+ +-+-+ +
|   |   |         | |
+ +-+ + +-+-+ +-+ + +
| |   |     |   |   |
+ + +-+-+-+ +-+-+-+-+
|       |   |       |
+-+-+-+ + + + +-+-+ +
|       | |   |      
+-+-+-+-+-+-+-+-+-+-+
""".strip()
maze_tmp = maze_ascii.replace("-","1").replace("+","1").replace("|","1").replace(" ","0")
mazearr = [[int(c) for c in line] for line in maze_tmp.split("\n")]

class maze:
    
    compass = {1:(-1,0),2:(-1,1),3:(0,1),4:(1,1),
               5:(1,0),6:(1,-1),7:(0,-1),8:(-1,-1)}
    
    def __init__(self,mazearr,startpos):
        self.pos = startpos
        self.maze = mazearr
        self.seen = []
        self.find_visible_blocks()
    
    def to_str(self,only_seen=True,scale=3):
        ret = ""
        for y in range(len(self.maze)):
            for i in range(scale):
                for x in range(len(self.maze[y])):
                    if self.maze[y][x] and ((not only_seen) or (y,x) in self.seen):
                        ret += "##"*scale
                    else:
                        if (y,x) == self.pos:
                            smaller = i+1 if i+1 < scale-i else scale-i
                            spacenum = 2*scale - smaller*2
                            ret += " "*(spacenum/2)
                            ret += "@"*(smaller*2)
                            ret += " "*(spacenum/2)
                        else:
                            ret += "  "*scale
                ret += "\n"
#        ret += "\n"
#        ret += " 8 1 2\n"
#        ret += "  \\|/\n"
#        ret += "7--0--3\n"
#        ret += "  /|\\\n"
#        ret += " 6 5 4\n"
        return ret
    
    def pos_ok(self,pos):
        ok  = pos[0] >= 0
        ok &= pos[1] >= 0
        ok &= pos[0] < len(self.maze)
        ok &= pos[1] < len(self.maze[0])
        return ok

    def move(self,direction):
        cy,cx = self.compass[direction]
        py,px = self.pos
        newpos = (py+cy,px+cx)
        if not self.pos_ok(newpos):
            return
        if not self.direction_visible(self.pos,direction):
            return
        if self.maze[newpos[0]][newpos[1]]:
            return
        self.pos = newpos
        self.find_visible_blocks()

    # This function will return True if the nearest tile
    # in the provided direction will be visible to
    # the person in the given position.
    def direction_visible(self,pos,direction):
        if direction % 2:
            return True
        for d in [direction-1,(direction+1)%8]:
            py,px = pos
            cy,cx = self.compass[d]
            b = (py+cy,px+cx)
            if self.pos_ok(b) and not self.maze[py+cy][px+cx]:
                return True
        return False

    def find_visible_spaces(self):
        vis = [(0,self.pos)]
        for d,v in self.compass.items():
            pos = (self.pos[0]+v[0],self.pos[1]+v[1])
            while self.pos_ok(pos):
                if self.maze[pos[0]][pos[1]]: break
                vis.append((d,pos))
                if not self.direction_visible(pos,d): break
                pos = (pos[0]+v[0],pos[1]+v[1])
        return vis
    
    def find_visible_blocks(self):
        vis = []
        for d,s in self.find_visible_spaces():
            if not d:
                vis.append(s)
                for cd,cv in self.compass.items():
                    b = (s[0]+cv[0],s[1]+cv[1])
                    if self.direction_visible(s,cd):
                        vis.append(b)
                continue
            dirs = [((d-2)%8)+1,d,(d%8)+1]
            for sd in dirs:
                b = (s[0]+self.compass[sd][0],s[1]+self.compass[sd][1])
                if self.direction_visible(s,sd):
                    vis.append(b)
        for v in vis:
            if v not in self.seen:
                self.seen.append(v)
        return vis

m = maze(mazearr,(1,0))
print "\n"*50
print m.to_str()

while True:
    ch = raw_input()
    if ch not in ["w","a","s","d"]:
        continue
    elif ch == "d" : m.move(3)
    elif ch == "a" : m.move(7)
    elif ch == "w" : m.move(1)
    elif ch == "s" : m.move(5)
    print "\n"*50
    print m.to_str()
    





















