import math

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z     
        
    def __sub__(self, other):
        return Point(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )      
        
    def dot(self, other):
        return (
            self.x * other.x +
            self.y * other.y +
            self.z * other.z
        )      
        
    def cross(self, other):
        return Point(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )     
        
    def absolute(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

def plane_angle(a, b, c, d):
    AB = b - a
    BC = c - b
    CD = d - c

    N1 = AB.cross(BC)
    N2 = BC.cross(CD)

    dot_product = N1.dot(N2)


    len_N1 = N1.absolute()
    len_N2 = N2.absolute()


    if len_N1 == 0 or len_N2 == 0:
        return 0.0
    
    cos_phi = dot_product / (len_N1 * len_N2)
    cos_phi = max(min(cos_phi, 1.0), -1.0)
    phi_rad = math.acos(cos_phi)
    angle_deg = math.degrees(phi_rad)
    if angle_deg > 90:
        angle_deg = 180 - angle_deg
    return angle_deg


if __name__ == '__main__':
    points = []
    for _ in range(4):
        x, y, z = map(float, input().split())
        points.append(Point(x, y, z))

    A, B, C, D = points

    result = plane_angle(A, B, C, D)
    print(f"{result:.1f}")
