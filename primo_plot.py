# primo_plot.py - a script designed to read in and plot primogem history
#                reads in a file "primo_data.tsv" with a particular format
#                displays output plot, will have to manually save 

import matplotlib.pyplot as plt
from matplotlib import patches


# Initialize some plot-oriented variables
lastDay = 375             # Index of final data point
beginPlot = -2            # Lower limit of x-axis to display
endPlot = 384             # Upper limit of x-axis to display
topPlot = 52000           # Upper limit of y-axis to display
bottomBannerBox = 48500   # Y-coordinate where upper banner labels begin
bannerTextPos = 50000     # Y-coordinate where banner label text sits


# Declare primogem value variables that will be incremented/overwritten 
totalGained = 0           # Running total of how many primogems were gained
totalUsed = 0             # Running total of how many primogems were used
lastAmount = 0            # Value of previous day's primogems for comparisons


# Declare list variables that will store data for plotting
day_lis = []              # Index of data points (x-axis)
primo_lis = []            # Value of data points (y-axis)

pull_date = []            # Index of pull dates (x-axis)
pull_amt = []             # Value of pulls (y-axis)


# Declare & hard-code banner labels that will be displayed on plot
#     Banners with multiple 5* have a newline character ('\n') in the string
banner_tick = []
banner_labels = ["Shenhe\nXiao", "Zhongli\nGanyu","Yae Miko","Raiden\nKokomi","Ayato\nVenti","Ayaka","Yelan\nXiao","Itto","Kazuha\nKlee","Yoimiya","Tighnari\nZhongli","Ganyu\nKokomi","Cyno\nVenti","Nilou\nAlbedo","Nahida\nYoimiya","Yae Miko\nTartaglia","Wanderer\nItto","Raiden\nAyato"]


# Hard-code where each month will appear on the plot (x-axis labels)
month_tick = [0,33,63,94,124,156,186,218,249,280,312,343]
month_labels = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]


# Input file to read in
infile_name = "primo_data.tsv"
infile = open(infile_name, 'r')


# Reading in data
i = 0
for line in infile:
    
    # Skip column headers
    if (i == 0):
        i += 1
        continue
    
    # Stop reading at a particular index. Useful if you have incomplete rows
    if (i == lastDay):
        break
    
    # Split .tsv file by tab characters ('\t')
    split = line[:-1].split("\t")
    
    # Assumes the following structure to lines being read in:
    #   [0]     [1]        [2]            [3]
    #   Date   Day #    New Banner?  Primogem Value
    #        (x-coord)                 (y-coord)

    # Save x-coordinate for plot
    day_lis.append(float(split[1]))
    
    # Save the index where a new banner occurs
    if (split[2] == "T"):
        banner_tick.append(i-1)

    # Save y-coordinate for plot
    amount = int(split[3])
    primo_lis.append(amount)

    # Compare current primogem value to the previous day's value
    if (i == 1): # Base case
        lastAmt = amount
    else:
        # If primogems were gained, add to the running total
        if (amount > lastAmt):
            totalGained += amount-lastAmt
            lastAmt = amount
            
        # If primogems were used, add to the running total
        else:
            totalUsed += lastAmt - amount
            lastAmt = amount

    # Find and save pull dates
    if (primo_lis[i-1] < primo_lis[i-2]):
        pull_date.append((i-2,i-1))
        pull_amt.append((primo_lis[i-2],primo_lis[i-1]))
    i += 1
    

# Print some totals out to console
print("Total Amount of Primogems Gained:",totalGained)
print("Daily Average Primogems Gained:",totalGained/365.0)
print("Total Amount of Primogems Used:",totalUsed)
    
infile.close()


# Constructing the plot
fig, ax = plt.subplots()


# Labeling the banners running across the top of the plot
for i in range(len(banner_labels)):

    # Condition for final banner 
    if (i == len(banner_labels)-1):
        # Text is placed with the following arguments:
        # (x position, y position, label text, horizontal align, vertical align)
        # x position is midway between banner start and end of x range
        ax.text((banner_tick[i]+endPlot)/2,bannerTextPos,banner_labels[i],horizontalalignment="center",verticalalignment="center")
        
    # Condition for all other banners
    else:
        # Same arguments as final banner condition except for:
        # x position is midway between banner start and banner end
        ax.text((banner_tick[i]+banner_tick[i+1])/2,bannerTextPos,banner_labels[i],horizontalalignment="center",verticalalignment="center")

    # Add in vertical dotted separation lines between banners
    # Arguments are as follows:
    # (x position, y start, y end, linestyle, color)
    plt.vlines(banner_tick[i],0,topPlot,linestyles="dotted",colors="black")

    
# Add in a horizontal dashed line across the bottom of the plot
# Arguments are as follows:
# (y position, x start, x end, linestyle, color)
plt.hlines(0,0,endPlot,linestyles="dashed",colors="black")


# Plotting main curve
# Arguments are as follows:
# ([x positions], [y values], linewidth, label)
plt.plot(range(len(primo_lis)), primo_lis, lw=5, label="Primogems Gained")


# Overplotting pulls
for i in range(len(pull_date)):
    # Plots each pull attempt as a separate call to plt.plot
    pull_start_date, pull_end_date = pull_date[i]
    pull_start_amt, pull_end_amt = pull_amt[i]
    
    # Include label argument in first pull curve for use in the legend
    #   (Otherwise each curve will have its own entry in the legend)
    # Arguments are as follows:
    # ([x(start), x(end)], [y(start), y(end)], color, linewidth, label)
    if (i == 0): 
        plt.plot([pull_start_date, pull_end_date], [pull_start_amt, pull_end_amt], 'r', lw=4, label="Primogems Used")
    else:
        plt.plot([pull_start_date, pull_end_date], [pull_start_amt, pull_end_amt], 'r', lw=4)


# Background color for banner placements
# Rectangular Patch added to plot, arguments are as follows:
# ((x pos (lower left), y pos (lower left)), width, height, color, opacity, label)
ax.add_patch(patches.Rectangle((beginPlot,bottomBannerBox),endPlot-beginPlot,4000,color="g",alpha=0.2,label="Banners"))


# Place vertical lines at start/end of year
plt.vlines(-1,0,bottomBannerBox,linestyles="solid",colors="black",lw=4)
plt.vlines(lastDay-1,0,bottomBannerBox,linestyles="solid",colors="black",lw=4,label="Start/End of Year")


# Setting global plot values
fig.set_size_inches(18,8) # Figure size in inches
fig.set_dpi(160)          # Figure pixel density (100 is default)

# Setting x-axis ticks/labels as calendar months
ax.set_xticks(month_tick)
ax.set_xticklabels(month_labels)

# Placing the legend
plt.legend(loc="upper right", bbox_to_anchor=(0.97,0.92),framealpha=1.0)

# Specifying x & y limits
plt.xlim(beginPlot,endPlot)
plt.ylim(0,topPlot)

# Axes labels
plt.ylabel("Primogem Amount", fontsize=20)
plt.xlabel("Month", fontsize=20)

# Display plot
plt.show()

# Could add a plt.savefig("<filename.png>") if wanted
