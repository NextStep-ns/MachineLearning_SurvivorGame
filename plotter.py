from IPython import display
import matplotlib.pyplot as plt
import numpy as np

plt.ion()

def plot(scores,cow, knife):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title("Training...")
    plt.xlabel("Number of Games")
    plt.ylabel("Score")
    plt.plot(scores)
    plt.plot(cow)
    #plt.plot(knife)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1,scores[-1],str(scores[-1]))
    plt.text(len(cow)-1, cow[-1], str(cow[-1]))
    #plt.text(len(knife) - 1, knife[-1], str(knife[-1]))
    plt.show(block=False)
    plt.pause(.1)

def hist(actions):
    # Clear previous plot
    plt.clf()
    
    # Plot histogram
    labels = ['STAY', 'RIGHT', 'DOWN', 'LEFT', 'UP', 'INTERACT']
    num_actions = len(labels)
    plt.hist(actions, bins=num_actions, align='left', range=(0, num_actions), rwidth=0.8)
    
    # Add labels and title
    plt.title("Actions")
    plt.xlabel("Action")
    plt.ylabel("Amount")
    plt.ylim(0,50)

    # Set x-axis tick locations and labels
    plt.xticks(range(num_actions), labels)

    # Show the plot
    plt.show(block=False)
    plt.pause(.1)