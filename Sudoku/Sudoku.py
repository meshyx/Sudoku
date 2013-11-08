import copy
import itertools

class Sudoku():
    def __init__(self, boardstring):
        self.size = int(len(boardstring)**0.5)
        self.bsize = int(self.size**0.5)
        if (self.size == 4):
            self.values = set([str(x) for x in range(1, 5)])
        if (self.size == 9):
            self.values = set([str(x) for x in range(1, 10)])
        if (self.size == 16):
            self.values = set([str(x) for x in range(0, 10)] + [chr(x) for x in range(ord('A'), ord('G'))])
        if (self.size == 25):
            self.values = set([str(x) for x in range(0, 10)] + [chr(x) for x in range(ord('A'), ord('P'))]) 
        self.board = []
        for val in list(boardstring):
            if (val == '.'):
                self.board.append(copy.deepcopy(self.values))
            else:
                self.board.append(set(val))
        rows = [x for x in range(self.size)]
        cols = [x * self.size for x in range(self.size)]
        boxes = [y * self.bsize + x * self.bsize * self.size for x in range(self.bsize) for y in range(self.bsize)]
        self.units = [[r + c for r in rows] for c in cols] + [[r + c for c in cols] for r in rows] + [[r + c * self.size + b for c in range(self.bsize) for r in range(self.bsize)] for b in boxes]

    def __str2__(self):
        b = ''
        longest = max(max([len(x) for x in self.board]), 3)
        for i in range(81):
            tempstring = ''
            for n in self.board[i]:
                tempstring += str(n)
            b += tempstring.center(longest)
            if (i == 26 or i == 53):
                b += '\n' + '-' * longest * 3 + '+'  + '-' * longest * 3 + '+'  + '-' * longest * 3
            if (i % 9 == 2 or i % 9 == 5):
                b += '|'
            if (i % 9 == 8):
                b += '\n'
        return b

    def __str__(self):
        s = ''
        longest = max(max([len(x) for x in self.board]), 3)
        for i in range(self.size * self.size):
            tempstring = ''
            for n in self.board[i]:
                tempstring += str(n)
            s += tempstring.center(longest)
            if (i % self.size == self.size - 1):
                s += '\n'
                if (i != (self.size * self.size) - 1 and i % (self.size * self.bsize) == (self.size * self.bsize) - 1):
                    s += '-' * self.bsize * longest
                    for n in range(self.bsize - 1):
                        s += '+' + '-' * self.bsize * longest
                    s += '\n'
            elif (i % self.bsize == self.bsize - 1):
                s += '|'
        return s
    
    def checkvalid(self):
        if any(len(self.board[i]) != 1 for i in range(self.size * self.size)):
            return False
        for unit in self.units:
            candidates = []
            for loc in unit:
                candidates += list(self.board[loc])
            if (set(candidates) != self.values):
                return False
        return True

    def nakedsingle(self):
        didwork = False
        for unit in self.units:
            for loc1 in unit:
                if (len(self.board[loc1]) == 1):
                    for loc2 in unit:
                        if (loc2 != loc1):
                            if (next(iter(self.board[loc1])) in self.board[loc2]):
                                self.board[loc2] -= self.board[loc1]
                                didwork = True
        return didwork

    def hiddensingle(self):
        didwork = False
        for unit in self.units:
            candidates = []
            for loc in unit:
                candidates += list(self.board[loc])
            for loc in unit:
                if (len(self.board[loc]) != 1):
                    for num in self.board[loc]:
                        if (candidates.count(num) == 1):
                            self.board[loc] = {num}
                            didwork = True
        return didwork

    def nakedpair(self):
        didwork = False
        for unit in self.units:
            for loc1 in unit:
                for loc2 in unit:
                    if ((loc1 != loc2) and len(self.board[loc1]) == 2 and len(self.board[loc2]) == 2 and self.board[loc1] == self.board[loc2]):
                        for num in self.board[loc1]:
                            for loc3 in unit:
                                if (loc3 != loc2 and loc3 != loc1 and num in self.board[loc3]):
                                    self.board[loc3].discard(num)
                                    didwork = True
        return didwork

    def OLDhiddenpair(self):
        didwork = False
        for unit in self.units:
            for loc1 in unit:
                for loc2 in unit:
                    if (len(self.board[loc1]) >= 2 and len(self.board[loc2]) >= 2):
                        isect = self.board[loc1].intersection(self.board[loc2])
                        if (len(isect) >= 2):
                            isectpairs = itertools.permutations(isect, 2)
                            for pair in isectpairs:
                                pair = set(pair)
                                alone = True
                                for loc3 in unit:
                                    if (loc3 != loc2 and loc3 != loc1 and not pair.isdisjoint(self.board[loc3])):
                                        alone = False
                                if (alone == True):
                                    self.board[loc1] = copy.deepcopy(pair)
                                    self.board[loc2] = copy.deepcopy(pair)
                                    didwork = True
        return didwork                            

    def hiddenpair(self):
        for unit in self.units:
            candidates = []
            for loc in unit:
                if (len(self.board[loc]) >= 2):
                    candidates += list(self.board[loc])
            numintwo = []
            for num in set(candidates):
                if (candidates.count(num) == 2):
                    numintwo += num
            if (len(numintwo) >= 2):
                pairs = itertools.permutations(numintwo, 2)
                for pair in pairs:
                    for pair in pairs:
                        pair = set(pair)
                        hits = []
                        for loc in unit:
                            if (len(self.board[loc]) >= 2):
                                if (pair.issubset(self.board[loc])):
                                    hits.append(loc)
                                    if (len(hits) == 2 and (len(self.board[hits[0]]) >= 3 or len(self.board[hits[1]]) >= 3)):
                                        self.board[hits[0]] = copy.deepcopy(pair)
                                        self.board[hits[1]] = copy.deepcopy(pair)
                                        return True
        return False
        
    def solveverbose(self):
        while 1:
            if (self.checkvalid()):
                print('valid')
                print(self)
                return True
            result = self.nakedsingle()
            print('naked single', result)
            print(self)
            input('Press enter\n')
            if (result):
                continue
            result = self.hiddensingle()
            print('hidden single', result)
            print(self)
            input('Press enter\n')
            if (result):
                continue
            result = self.nakedpair()
            print('naked pair', result)
            print(self)
            input('Press enter\n')
            if (result):
                continue
            result = self.hiddenpair()
            print('hidden pair', result)
            print(self)
            input('Press enter\n')
            if (result):
                continue
        
    def solve(self):
        while not (self.checkvalid()):
            self.nakedsingle()
            self.hiddensingle()
            self.nakedpair()
            self.hiddenpair()
        return True

    def recsolve(self, loc = 0):
        if (loc == 81):
            return True
        if (len(self.board[loc]) == 1):
            return self.solve(loc + 1)
        else:
            originalset = self.board[loc]
            for num in self.board[loc]:
                print(self)
                self.iter += 1
                if (self.testrow(loc, num) and self.testcol(loc, num) and self.testbox(loc, num)):
                    self.board[loc] = set([num])
                    if (self.solve(loc + 1)):
                        return True
            self.board[loc] = originalset
        return False


#boardstring = '53..97..........7.....1..5......13....4..2...1.98..2.4........5.7....92..91.5....'
#boardstring = '7..25..98..6....1....61.3..9....1.......8.4.9..75.28.1.94..3.......4923.61.....4.'
#boardstring = '..41..3.8.1....62...82..4.....3.28.9....7....7.16.8...562..17.3.3.....4.1....5...'
#boardstring = '1.......4....1.38.27.9.4...91.7...........5..86.4.5.9..3......8..9....2.4.......7'
#boardstring = '7..25..98..6....1....61.3..9....1.......8.4.9..75.28.1.94..3.......4923.61.....4.'
#boardstring = '..............3.85..1.2.......5.7.....4...1...9.......5......73..2.1........4...9'
#boardstring = '.2.....7.9..5.8..4.........4...3...8.7..9..2.6...1...5.........5..6.4..1.3.....9.'
#boardstring = '.395........8...7.....1.9.41..4....3...........7...86...67.82...1..9...5.....1..8'
#boardstring = '.94...13..............76..2.8..1.....32.........2...6.....5.4.......8..7..63.4..8'
#boardstring = '.........9.46.7....768.41..3.97.1.8.7.8...3.1.513.87.2..75.261...54.32.8.........'
#boardstring = '123423413412....'
#boardstring = '..B5..6.H.4N.90..3.......1.I.C...9........H4.....0.......L....2.1..DB.F7O...F...1M..CBL...KEI2....D.M.N.....O73.FIK..6...2B.8.3.1.......9.NBGF...4......8..5O...7.42......J..HIE.9A...HBI.......M..6..3........D.L..HFJ.5AC.......L.O..0G436..D.72K..A...5.JCE......8..1.O.07..4.K..0....F9.6..3J..8..D.N.G.O14.....C.....L.....I07....6K..B.1G...H5F..E..C.9.79HBF8...4....I..G.K.E..L.7..E.2.5.K..6.HD4.0........I.0.FA...9LOE......K...20.K..3....1.C.NO..D..5........E.BD.5GN.......C...4MF3.CN61.8..E2.L......7..OJ1.I....0....K2..B....FB.4.AK.M..E....I8.....O9....8JL63.2.DOH.A.....0.EN.5.L7.OD.9A.8.J0F.6.M..CDCK0..4...5.L.M9...1..H6A'
#boardstring = '2....F37.............C5E....DF...E1.B......2.9.CD056.2...F9..A...A.37.B..2D01..917.B5..A98.3...E8.....D.....4.F..6.531C2.....8.7A9.2...F.B....56B.......D......F..E......476B.8....7...8CE...D..7..8..1..9...2A...BF8..3..AD.76..C...6A5F7....0......D..E..5.C3.'
boardstring = ' 6 . 15 . . 8 16 . 10 . . . 1 . 7 3 . . 10 16 . . 13 2 6 . . . . . 9 . . . . 14 . 9 . 7 . 4 . 5 . . 10 . . 12 5 9 . 15 . . . . 11 . 6 . . . . . 12 . 11 5 . . 16 . . . 9 6 . . . 1 . 4 2 12 . . . 11 15 . 5 . . . . . . 5 . . . 3 . . 2 4 . 15 11 . . 15 8 . . . 10 13 . 6 9 14 . . . 4 3 . . 12 . . . 4 9 . 5 13 . . 1 . . 13 . 10 . . . . . . 12 . 16 . . . . . . . . 13 . . 4 . . . 2 . . . 9 . 14 . . 3 8 . 1 . . 16 . 4 . 5 . 6 . . . . . . . . . 10 . 3 . 11 . 5 4 . . . 2 . . 12 16 . . . 13 . 2 . 3 . 14 1 . 10 . . . . 12 . 16 . . 10 . . 12 . . . . . 8 . . 9 . 15 '.replace(' 1 ', ' 0 ').replace(' 2 ', ' 1 ').replace(' 3 ', ' 2 ').replace(' 4 ', ' 3 ').replace(' 5 ', ' 4 ').replace(' 6 ', ' 5 ').replace(' 7 ', ' 6 ').replace(' 8 ', ' 7 ').replace(' 9 ', ' 8 ').replace(' 10 ', ' 9 ').replace(' 11 ', ' A ').replace(' 12 ', ' B ').replace(' 13 ', ' C ').replace(' 14 ', ' D ').replace(' 15 ', ' E ').replace(' 16 ', ' F ').replace(' ', '')


sudoku = Sudoku(boardstring)
sudoku.solveverbose()
#===============================================================================
# if (sudoku.solve):
#     print(sudoku)
#===============================================================================