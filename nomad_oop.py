class Dog:

    def __init__(self, name, age, breed):
        self.name = name
        self.age = age
        self.breed = breed
    
    def sleep(self):
        print("Zzzzzzz.....")

class GuardDog(Dog):

    def __init__(self, name, breed):
        super().__init__(name, 5, breed)
        self.aggresive = True

    def rrrrr(self):
        print("stay away!!")


class Puppy(Dog):

    def __init__(self, name, breed): # method: 클래스안에 있는 함수, self를 첫번째 인자로 가져야함
        super().__init__(name, 0.1, breed)
        self.spoiled = True

    def __str__(self): # print class instance
        return f"{self.breed} puppy named {self.name}"
    
    def woof_woof(self):
        print("Woof Woof!")

    def introduce(self):
        self.woof_woof()
        print(f"My name is {self.name} and I am a baby {self.breed}")


ruffus =Puppy(name="Ruffus", breed="Beagle")
bibi = GuardDog(name="Bibi", breed="Dalmatian")

# print(ruffus, bibi)
ruffus.woof_woof()
bibi.rrrrr()

ruffus.sleep()
bibi.sleep()