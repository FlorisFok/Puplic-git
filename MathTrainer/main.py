import sys
import random
import time

class Calculation:
    
    #LOCAL VARS
    
    
    def __init__(self, level, sleep_time, mode):
        self.level = level
        self.sleep_time = sleep_time
        self.mode = mode


    def difficult_level(self):
        num = random.randint(1,50)
        num2 = random.randint(1,50)
        return num*(10**self.level), num2*(10**self.level)


    def sumnum(self):
        num, num2 = self.difficult_level()
        print(f"What is: the sum of {num} and {num2}")
        
        if self.mode == 'test':
            time.sleep(self.sleep_time)
            print(str(num+num2))
        else:
            return num+num2

        
    def percentage(self):
        num, num2 = self.difficult_level()
        if num2 > 100:
            while num2 > 100:
                num2 = num2/10
        print(f"What is: {num} times {num2}%")

        if self.mode == 'test':
            time.sleep(self.sleep_time)
            print(str(num*(num2*0.01)))
        else:
            return num*(num2*0.01)

        
    def division(self):
        num, num2 = self.difficult_level()
        if num > num2:
            print(f"What is: {num} divided by {num2/10}")
            
            if self.mode == 'test':
                time.sleep(self.sleep_time)
                print(str(num/(num2/10)))
            else:
                return num/(num2/10)
        else:
            print(f"What is: {num2} divided by {num/10}")
            
            if self.mode == 'test':
                time.sleep(self.sleep_time)
                print(str(num2/(num/10)))
            else:
                return num2/(num/10)


    def multi(self):
        num, num2 = self.difficult_level()
        if num2 > 10**self.level*0.5:
            while num2 > 1000:
                num2 = num2/10

        print(f"What is: {num} times {num2/10}")
        
        if self.mode == 'test':
            time.sleep(self.sleep_time)
            print(str(num*(num2/10)))
        else:
            return num*(num2/10)


def test(level, sleep_time, mode):
    while True:
        cal  = Calculation(level, sleep_time, mode)
        option = random.randint(0,3)
        
        if option == 0:
            cal.sumnum()
        elif option == 1:
            cal.percentage()
        elif option == 2:
            cal.division()
        elif option == 3:
            cal.multi()
        
        anwser = input("Continue: (enter) & Quit: (y/yes)")
        if anwser == 'y' or anwser == 'yes':
            break


def train(level, setting, mode):

    cal  = Calculation(level, setting, mode)
    t = time.time()

    anwsers = []
    inputs = []
    for j in range(0,setting):
        anwsers.append(int(cal.sumnum()))
        try:
            inputs.append(int(input(":  ")))
        except:
            inputs.append('N.A')

    for j in range(0,setting):
        anwsers.append(int(cal.percentage()))
        try:
            inputs.append(int(input(":  ")))
        except:
            inputs.append('N.A')

    for j in range(0,setting):
        anwsers.append(int(cal.division()))
        try:
            inputs.append(int(input(":  ")))
        except:
            inputs.append('N.A')

    for j in range(0,setting):
        anwsers.append(int(cal.multi()))
        try:
            inputs.append(int(input(":  ")))
        except:
            inputs.append('N.A')
    
    print(f'Total time = {(time.time()-t)}')
    print('The correct anwsers and your anwsers are:')
    print(anwsers)
    print(inputs)

def main():
    level, setting, mode = usage()
    if mode == "test":
        print("Good luck, level is set to {} and sleep time to {}".format(level, setting))
        test(level, sleep, mode)
    else:
        print("Let's train and become a genius")
        print('*        *       *')
        print('level is {}'.format(level))
        train(level, setting, mode)

def usage():
    args = sys.argv

    if len(args) != 4:
        print("Usage: python main.py level (int) setting(int) 'train' or 'test'")
        sys.exit()
    try:
        level = int(args[1])
        sleep = int(args[2])
        mode = args[3]
        return level, sleep, mode
    except:
        print("Please enter intergers for leven and sleep_time")
        sys.exit()


if __name__ == '__main__':
    main()