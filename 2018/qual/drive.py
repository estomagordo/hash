from sys import argv

def solve(r, c, f, n, b, t, rides):
    cars = [[0, 0, 0, 0, 0, False] for _ in range(f)]
    out = [[0] for _ in range(f)]

    for step in range(t):
        for carnum in range(f):
            car = cars[carnum]
            y, x, dy, dx, steps, done = car
            
            if done:
                continue
            
            if y < dy:
                car[0] += 1
            elif y > dy:
                car[0] -= 1
            elif x < dx:
                car[1] += 1
            elif x > dx:
                car[1] -= 1
            else:
                if steps % 2 == 0:
                    delivered = steps // 2
                    nextrideindex = delivered * f + carnum
                    if nextrideindex >= n:
                        car[-1] = True
                        continue
                    nextride = rides[nextrideindex]
                    a, b, ry, rx, s, fi = nextride
                    if step < s:
                        continue
                    if step >= fi:
                        steps += 2
                        nextrideindex = (steps // 2) * f + carnum
                        if nextrideindex >= n:
                            car[-1] = True
                            continue
                        nextride = rides[nextrideindex]
                        car[2] = nextride[0]
                        car[3] = nextride[1]
                    else:
                        car[4] += 1
                        car[2] = nextride[2]
                        car[3] = nextride[3]
                else:
                    delivered = steps // 2
                    nextrideindex = delivered * f + carnum
                    nextride = rides[nextrideindex]
                    a, b, ry, rx, s, fi = nextride
                    if step <= fi:
                        out[carnum][0] += 1
                        out[carnum] += [nextrideindex]                        
                    car[4] += 1
                    steps += 1
                    nextrideindex = (steps // 2) * f + carnum
                    if nextrideindex >= n:
                        car[-1] = True
                        continue
                    nextride = rides[nextrideindex]
                    car[2] = nextride[2]
                    car[3] = nextride[3]

    file_out.write('\n'.join(' '.join(str(num) for num in line) for line in out))

if __name__ == '__main__':
    filename = argv[1]

    with open(filename + '.in') as file_in:
        r, c, f, n, b, t = list(map(int, file_in.readline().split()))
        rides = [list(map(int, file_in.readline().split())) for _ in range(n)]

        with open(filename + '.out', 'w') as file_out:
            solve(r, c, f, n, b, t, rides)