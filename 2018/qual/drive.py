from sys import argv
from heapq import heappush, heappop
from copy import deepcopy

best = 0

def write(score, assignments):
    print(-score)

    with open(filename + '.out', 'w') as file_out:
        file_out.write('\n'.join(' '.join(str(num) for num in [len(line)] + line) for line in assignments))

def distance(y, x, dy, dx):
    return abs(y - dy) + abs(x - dx)

def solve(r, c, f, n, b, t, rides):
    global best
    rides = [rides[x] + [x] for x in range(n)]

    rides.sort(key = lambda ride: ride[4])    

    runs = [[0, 0, 0, 0, 0, [[] for _ in range(f)]]]
    
    while runs:
        score, y, x, time, carnum, assignments = heappop(runs)

        newscore = score
        newassignments = deepcopy(assignments)

        for newridenum in range(n):
            ride = rides[newridenum]
            taken = False

            for line in assignments:
                if ride[-1] in line:
                    taken = True
                    break

            if taken:
                continue

            reaching = time + distance(y, x, ride[0], ride[1])
            length = distance(ride[0], ride[1], ride[2], ride[3])
            done = max(reaching, ride[4]) + length
            
            if done <= ride[5]:
                newscore -= length - (0 if reaching > ride[4] else b)                
                newassignments[carnum].append(ride[-1])
                
                if newscore < best:
                    best = newscore
                    write(newscore, newassignments)

        if carnum == f - 1:
            continue

        heappush(runs, [newscore, 0, 0, 0, carnum + 1, newassignments])

if __name__ == '__main__':
    filename = 'a_example'#argv[1]

    with open(filename + '.in') as file_in:
        r, c, f, n, b, t = list(map(int, file_in.readline().split()))
        rides = [list(map(int, file_in.readline().split())) for _ in range(n)]
        solve(r, c, f, n, b, t, rides)