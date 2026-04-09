from model import Player


zov = Player("zxc",1,100,0)

print(zov)

print(repr(zov))



print(zov.take_damage(5))

print(zov.add_experience(999))
print(zov)
print(repr(zov))
print(zov.add_experience(1000))
print(zov)
print(repr(zov))
