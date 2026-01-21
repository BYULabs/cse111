import math

cans = [
    ("#1 Picnic", 6.83, 10.16),
    ("#1 Tall", 7.78, 11.91),
    ("#2", 8.73, 11.59),
    ("#2.5", 10.32, 11.91),
    ("#3 Cylinder", 10.79, 17.78),
    ("#5", 13.02, 14.29),
    ("#6Z", 5.40, 8.89),
    ("#8Z short", 6.83, 7.62),
    ("#10", 15.72, 17.78),
    ("#211", 6.83, 12.38),
    ("#300", 7.62, 11.27),
    ("#303", 8.10, 11.11),
]

def main():
    for can in cans:
        name = can[0]
        radius = can[1]
        height = can[2]
        volume = can_vol(radius, height)
        area = can_area(radius, height)
        eff = volume / area
        print(f"{name} {eff:.2f}")

def can_vol(radius, height):
    volume = math.pi * radius ** 2 * height
    return volume

def can_area(radius, height):
    area = 2 * math.pi * radius * (radius + height)
    return area

if __name__ == "__main__":
    main()