from sys import argv
from heapq import heappush, heappop

best = 0
seen = {}

def coord_to_score(c, coord):
    return coord[0] * c + coord[1]

def score_to_coord(c, score):
    return (score // c, score % c)

def score_cut(cut):
    return (cut[2] + 1 - cut[0]) * (cut[3] + 1 - cut[1])

def valid_cuts(r, c, y, x, l, h):
    valid = []

    for width in range(1, h + 1):
        if x + width > c:
            break
        for height in range(1, h + 1):
            if y + height > r or width * height > h:
                break
            if 2 * l > width * height:
                continue
            
            tomato = 0
            mushroom = 0
            tasty = True
            
            for dy in range(y, y + height):
                if not tasty:
                    break
                for dx in range(x, x + width):                        
                    if grid[dy][dx] == 'T':
                        tomato += 1
                    else:
                        mushroom += 1

            if tomato < l or mushroom < l:
                tasty = False
            if tasty:
                valid.append((y, x, y + height - 1, x + width - 1))

    return valid

def cutcoord_to_score(f, cutcoord):
    return cutcoord[0] + cutcoord[1] * f + cutcoord[2] * f * f + cutcoord[3] * f * f * f

def score_to_cutcoord(f, score):
    y0 = score % f
    score //= f
    x0 = score % f
    score //= f
    y1 = score % f
    score //= f
    x1 = score 

    return (y0, x0, y1, x1)

def point_outside_cuts(point, cuts):
    for cut in cuts:
        if cut[0] <= point[0] <= cut[2] and cut[1] <= point[1] <= cut[3]:
            return False
    return True

def non_overlapping(cuts, newcut):
    for cut in cuts:
        if cut[0] <= newcut[0] <= cut[2] and cut[1] <= newcut[1] <= cut[3]:
            return False
        if cut[0] <= newcut[2] <= cut[2] and cut[1] <= newcut[3] <= cut[3]:
            return False
        if newcut[0] <= cut[0] <= newcut[2] and newcut[1] <= cut[1] <= newcut[3]:
            return False
        if newcut[0] <= cut[2] <= newcut[2] and newcut[1] <= cut[3] <= newcut[3]:
            return False
        if newcut[0] <= cut[0] and newcut[2] >= cut[2] and newcut[1] >= cut[1] and newcut[3] <= cut[3]:
            return False
        if cut[0] <= newcut[0] and cut[2] >= newcut[2] and cut[1] >= newcut[1] and cut[3] <= newcut[3]:
            return False
        if cut[0] <= newcut[0] <= cut[2] and cut[1] <= newcut[3] <= cut[3]:
            return False
        if cut[0] <= newcut[2] <= cut[2] and cut[1] <= newcut[1] <= cut[3]:
            return False
        if newcut[0] <= cut[0] <= newcut[2] and newcut[1] <= cut[3] <= newcut[3]:
            return False
        if newcut[0] <= cut[2] <= newcut[2] and newcut[1] <= cut[1] <= newcut[3]:
            return False

    return True

def solve(r, c, l, h, grid):
    global best, seen, count
    f = max(r, c)
    
    stack = []

    for y in range(r):
        for x in range(c):
            stack.append((0, coord_to_score(c, (y, x)), ()))

    while stack:
        score, coordscore, cutscores = heappop(stack)
        y, x = score_to_coord(c, coordscore)
        
        cuts = [score_to_cutcoord(f, score) for score in cutscores]

        signature = (coordscore, cutscores)
        if signature in seen and seen[signature] <= score:
            continue
        seen[signature] = score
        
        if len(seen) % 1000000 == 0:
            print(len(seen))

        if -score > best:
            print('New best!', -score)
            best = -score
            
            with open(name + '.out', 'w') as g:
                g.write('\n'.join(' '.join(str(entry) for entry in line) for line in [(len(cuts),)] + cuts))

            if best == r * c:
                return
        
        newcuts = valid_cuts(r, c, y, x, l, h)

        if not newcuts:
            continue
        for cut in newcuts:
            if non_overlapping(cuts, cut):
                cutscore = cutcoord_to_score(f, cut)
                morecutscores = tuple(sorted(list(cutscores) + [cutscore]))
                newscore = score - score_cut(cut)
                morecuts = [score_to_cutcoord(f, score) for score in morecutscores]            
                if cut[2] == r - 1 and cut[3] == c - 1:
                    cscore = coord_to_score(c, (r, c))
                    if not ((cscore, morecutscores) in seen and seen[(cscore, morecutscores)] <= newscore):
                        heappush(stack, (newscore, cscore, morecutscores))
                else:
                    for ny in range(cut[0], min(r, cut[2] + 4)):
                        for nx in range(min(c, cut[3] + 4)):
                            if ny > cut[2] or nx > cut[3]:
                                cscore = coord_to_score(c, (ny, nx))
                                if not ((cscore, morecutscores) in seen and seen[(cscore, morecutscores)] <= newscore) and point_outside_cuts((ny, nx), morecuts):
                                    heappush(stack, (newscore, cscore, morecutscores))            

if __name__ == '__main__':
    name = argv[1]
    
    with open(name + '.in') as f:
        r, c, l, h = list(map(int, f.readline().split()))
        grid = [f.readline().strip() for _ in range(r)]

        with open(name + '.out', 'w') as g:
            solve(r, c, l, h, grid)
