boomT = 10
player = 1

while boomT > 0:

    player = player % 3
    if player == 1:
        print("1st")
        discount = int(input())
        boomT -= discount
        player += 1

    if player == 2:
        print("2st")
        discount = int(input())
        boomT -= discount
        player += 1

    if player == 0:
        print("3st")
        discount = int(input())
        boomT -= discount
        player += 1

print(f"Game end {player} lost")    