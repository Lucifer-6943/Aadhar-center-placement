import rasterio
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Path to the GeoTIFF file with black pixels
aadhaar_density_tif = '/content/drive/MyDrive/hackathon/topic19/NTL/2022_India.tif'

# Read the GeoTIFF file
with rasterio.open(aadhaar_density_tif) as src:
    # Read the pixel data
    data = src.read(1)

    # Get coordinates of black pixels
    black_pixels = np.where(data == 0)
    black_pixel_coordinates = np.column_stack((black_pixels[0], black_pixels[1]))

    # Set initial number of candidate centers
    num_centers = 70
    final_cluster_centers = None

    while num_centers > 0:
        # Apply k-means clustering to black pixel coordinates
        kmeans = KMeans(n_clusters=num_centers, random_state=42)
        kmeans.fit(black_pixel_coordinates)

        # Get cluster centers and labels
        cluster_centers = kmeans.cluster_centers_
        labels = kmeans.labels_

        # Calculate the count of black pixels after clustering
        pixel_count = np.sum(data == 0)

        # Calculate the count of black pixels near cluster centers
        cluster_centers_row = np.round(cluster_centers[:, 0]).astype(int)
        cluster_centers_col = np.round(cluster_centers[:, 1]).astype(int)
        center_pixel_count = np.sum(data[cluster_centers_row, cluster_centers_col] == 0)

        print(f"Number of Centers: {num_centers}, Black Pixels: {pixel_count}, Centers Black Pixels: {center_pixel_count}")

        # Store the final cluster centers with reduced centers
        final_cluster_centers = cluster_centers

        # Reduce the number of candidate centers
        num_centers -= 7  # You can adjust the step size here

    # Visualize the final clustering results
    plt.figure(figsize=(10, 8))
    plt.imshow(data, cmap='gray')  # Display the original image
    plt.scatter(final_cluster_centers[:, 1], final_cluster_centers[:, 0], c='red', marker='o', s=50, label='Final Cluster Centers')  # Plot final cluster centers
    plt.colorbar(label='Pixel Value')
    plt.title('Final Cluster Centers with Black Pixels')
    plt.legend()
    plt.show()
