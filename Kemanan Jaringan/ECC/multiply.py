
def multiply(self, other):
    track = [(1, self)]
    while track[-1][0] + track[-1][0] < other:
        track.append ((track[-1][0] + track[-1][0], track[-1][1] + track[-1][1]))

    for tracker, result in reversed(track):
        if track[-1][0] + tracker <= other:
            track.append ((track[-1][0] + tracker, track[-1][1] + result))
            print(f'track: {track[-1][0]}, result: {track[-1][1]}')


multiply(3, 5000000000)