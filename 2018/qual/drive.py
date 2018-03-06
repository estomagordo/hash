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

    runs = [[0, 0, 0, 0, 0, 0, set(), [[] for _ in range(f)]]]
    
    while runs:
        score, y, x, time, carnum, ridenum, taken, assignments = heappop(runs)
        
        for newcarnum in range(carnum, f):
            for newridenum in range(ridenum, n):
                ride = rides[newridenum]

                if ride[-1] in taken:
                    continue

                reaching = time + distance(y, x, ride[0], ride[1])
                length = distance(ride[0], ride[1], ride[2], ride[3])
                done = max(reaching, ride[4]) + length
                
                if done <= ride[5]:
                    
                    score -= length + (0 if reaching > ride[4] else b)                
                    assignments[carnum].append(ride[-1])
                    y = ride[2]
                    x = ride[3]
                    time = done
                    taken.add(ride[-1])
                    
                    if score < best:
                        best = score
                        write(score, assignments)

                newassignments = deepcopy(assignments)
                newtaken = deepcopy(taken)
                heappush(runs, [score, y, x, time, carnum, newridenum + 1, newtaken, newassignments])
            
            ridenum = 0

if __name__ == '__main__':
    filename = argv[1]

    with open(filename + '.in') as file_in:
        r, c, f, n, b, t = list(map(int, file_in.readline().split()))
        rides = [list(map(int, file_in.readline().split())) for _ in range(n)]
        solve(r, c, f, n, b, t, rides)