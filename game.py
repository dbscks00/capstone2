num = 5
life = 3
trys = 1

print("############숫자 맞추기 게임###########\n")

while life > 0:
    guess = int(input(f"{trys} 번째 추축: "))
    if guess == num:
        print("정답입니다")
        break
    else:
        print("틀렸습니다")
        if guess > num:
            print("정답은 더 작습니다")
        else : print("정답은 더 큽니다")
            
        life -= 1
        trys += 1
        
print("게임이 종료되었습니다.")