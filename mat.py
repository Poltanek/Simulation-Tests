import matplotlib.pyplot as plt

# Mock route data
route = [(37.7749, -122.4194), (37.7800, -122.4150), (37.7849, -122.4094)]

# Plot the route
lat, lon = zip(*route)
plt.plot(lon, lat, marker='o', label='Planned Route')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Pathfinding Algorithm Output')
plt.legend()
plt.show()
