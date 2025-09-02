import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def load_and_plot_gps_track(csv_file, line_length=0.001):
    """
    Load GPS track data from CSV and plot points with heading indicators.

    Parameters:
    csv_file (str): Path to CSV file with columns: lat, long, altitude, heading
    line_length (float): Length of heading lines in degrees (adjust based on your data scale)
    """

    # Load the CSV data
    try:
        df = pd.read_csv(csv_file)
        print(f"Loaded {len(df)} GPS points")
        print(f"Columns: {list(df.columns)}")
        print(f"Data preview:\n{df.head()}")
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    # Check if required columns exist (flexible column naming)
    lat_col = None
    lon_col = None
    heading_col = None

    for col in df.columns:
        col_lower = col.lower().strip()
        if 'latitude' in col_lower:
            lat_col = col
        elif 'longitude' in col_lower or 'long' in col_lower:
            lon_col = col
        elif 'course' in col_lower:
            heading_col = col

    if not all([lat_col, lon_col, heading_col]):
        print("Error: Could not find required columns (latitude, longitude, course)")
        print("Available columns:", list(df.columns))
        return

    # Extract data
    lats = df[lat_col].values
    lons = df[lon_col].values
    headings = df[heading_col].values

    # Apply headings to previous points (shift headings forward by 1)
    # This means each point shows the heading it had when leaving that point
    shifted_headings = np.zeros_like(headings)
    shifted_headings[0:] = headings[0:]

    # Summer method, shifting headings back one
    shifted_headings[:-1] = headings[1:]  # Apply next point's heading to current point
    shifted_headings[-1] = headings[-1]  # Last point keeps its own heading

    # Convert headings to radians (assuming headings are in degrees, 0° = North)
    # Note: In navigation, 0° is North, but in math, 0° is East
    # We need to convert: navigation heading to mathematical angle
    heading_rad = np.radians(90 - shifted_headings)  # Convert to math convention

    # Calculate end points for heading lines
    end_lats = lats + line_length * np.sin(heading_rad)
    end_lons = lons + line_length * np.cos(heading_rad)

    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 12))

    # Plot the track points
    ax.scatter(lons, lats, c='red', s=.1, alpha=0.7, label='GPS Points', zorder=3)

    # Plot heading lines
    for i in range(len(lats)):
        ax.plot([lons[i], end_lons[i]], [lats[i], end_lats[i]],
                'blue', linewidth=1, alpha=0.6)

    # Connect points to show track
    ax.plot(lons, lats, 'gray', linewidth=0.5, alpha=0.5, label='Track', zorder=1)

    # Formatting
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('GPS Track with Headings')
    ax.grid(True, alpha=0.3)
    ax.legend()

    # Make axes equal for proper geographic representation
    ax.set_aspect('equal', adjustable='box')

    # Add some statistics
    print(f"\nTrack Statistics:")
    print(f"Latitude range: {lats.min():.6f} to {lats.max():.6f}")
    print(f"Longitude range: {lons.min():.6f} to {lons.max():.6f}")
    print(f"Heading range: {headings.min():.1f}° to {headings.max():.1f}°")

    plt.tight_layout()
    plt.show()

    return df


def plot_with_custom_settings(csv_file, line_length=0.001, point_size=20,
                              line_color='blue', point_color='red'):
    """
    More customizable version of the plotting function.
    """
    df = pd.read_csv(csv_file)

    # Auto-detect columns (same logic as above)
    lat_col = lon_col = heading_col = None
    for col in df.columns:
        col_lower = col.lower().strip()
        if 'lat' in col_lower:
            lat_col = col
        elif 'lon' in col_lower or 'long' in col_lower:
            lon_col = col
        elif 'head' in col_lower:
            heading_col = col

    lats = df[lat_col].values
    lons = df[lon_col].values
    headings = df[heading_col].values

    # Convert headings
    heading_rad = np.radians(90 - headings)
    end_lats = lats + line_length * np.sin(heading_rad)
    end_lons = lons + line_length * np.cos(heading_rad)

    # Create plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Left plot: Full track
    ax1.scatter(lons, lats, c=point_color, s=point_size, alpha=0.7, zorder=3)
    for i in range(len(lats)):
        ax1.plot([lons[i], end_lons[i]], [lats[i], end_lats[i]],
                 line_color, linewidth=1, alpha=0.6)
    ax1.plot(lons, lats, 'gray', linewidth=0.5, alpha=0.5, zorder=1)
    ax1.set_title('Full GPS Track')
    ax1.set_xlabel('Longitude')
    ax1.set_ylabel('Latitude')
    ax1.grid(True, alpha=0.3)
    ax1.set_aspect('equal')

    # Right plot: Heading distribution
    ax2.hist(headings, bins=36, alpha=0.7, edgecolor='black')
    ax2.set_title('Heading Distribution')
    ax2.set_xlabel('Heading (degrees)')
    ax2.set_ylabel('Frequency')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    return df


# Example usage:
if __name__ == "__main__":
    # Replace 'your_file.csv' with your actual CSV file path
    csv_filename = "FSGP_2024_Pregenerated.csv"

    print("GPS Track Visualization")
    print("=" * 30)

    # Basic usage
    df = load_and_plot_gps_track(csv_filename, line_length=0.000005)

    # Advanced usage with custom settings
    # df = plot_with_custom_settings(csv_filename,
    #                               line_length=0.002,
    #                               point_size=15,
    #                               line_color='green',
    #                               point_color='blue')

    print("\nTo use this script:")
    print("1. Update 'csv_filename' with your file path")
    print("2. Uncomment one of the function calls above")
    print("3. Adjust line_length parameter based on your data scale")
    print("   - For city-level data: try 0.001-0.005")
    print("   - For regional data: try 0.01-0.05")
    print("   - For country-level data: try 0.1-0.5")