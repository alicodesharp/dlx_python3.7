import main

design = main.DesignDLX(2,7,3)  # (7-3-1) BIBD

"""
V = 7, K = 3 , 
Örnek çözüm:
    {
    {1,2,4},{2,3,5},{3,4,6},{4,5,0},{5,6,1},{6,0,2},{0,1,3}
    }
"""

print(design.C)
print(design.D)
print(design.L)
print(design.N)
print(design.S)
print(type(design.solve()))
print(design.solve().__next__())

# Dönen generator nesnesinde iter yapabiliriz.
