import numpy as np
import matplotlib.pyplot as plt
import os

# The path of data
path = '/dtu/projects/02613_2025/data/modified_swiss_dwellings'

# Randomly select a few buildings
building_ids = [
    '11427', '179', '28701', '4475', '51314', '8298',
    '11430', '1802', '28704', '44799', '51316', '8308'
]

output_folder = 'Task_1'
os.makedirs(output_folder, exist_ok=True)

for building_id in building_ids:
    print(f"Processing building ID: {building_id} ...")
    
    # Load the files
    domain = np.load(f"{path}/{building_id}_domain.npy")
    interior = np.load(f"{path}/{building_id}_interior.npy")

    # Create the plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Display the initial temperature distribution
    im0 = axes[0].imshow(domain, cmap='inferno')  
    axes[0].set_title(f"Initial Temperature Grid (ID: {building_id})")
    fig.colorbar(im0, ax=axes[0], orientation='vertical', label='Temperature') 

    # Display the interior region mask
    im1 = axes[1].imshow(interior, cmap='gray')  
    axes[1].set_title(f"Interior Mask (ID: {building_id})")
    fig.colorbar(im1, ax=axes[1], orientation='vertical', label='Mask')  

    plt.tight_layout()
    
    # Save as an image format 
    save_filename = os.path.join(output_folder, f'task1_visualization_{building_id}.png')
    plt.savefig(save_filename, dpi=300, bbox_inches='tight')
    
    # Close the current figure at the end of each iteration to free memory
    plt.close(fig)

print("All images have been successfully processed and saved to the current directory!")