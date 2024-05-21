from IPython import display
import matplotlib.pyplot as plt
import numpy as np

plt.ion()

def plot(carrot_scores,cow_scores,knife_scores,agent,game):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    per=100*agent.epsilon/(agent.epsilon+agent.n_games)
    if per<0:
        per=0
    plt.title(f"Randomness : {round(per,1)}%, Cow rew : {game.COW_REWARD}, Knife rew : {game.KNIFE_REWARD}")
    plt.xlabel("Number of Games")
    plt.ylabel("Score")
    plt.plot(carrot_scores,label="Carrots")
    plt.plot(cow_scores,label="Cows")
    plt.plot(knife_scores,label="Knifes")
    plt.legend()
    plt.ylim(ymin=0)
    plt.text(len(carrot_scores)-1,carrot_scores[-1],str(carrot_scores[-1]))
    plt.text(len(cow_scores)-1,cow_scores[-1],str(cow_scores[-1]))
    plt.text(len(knife_scores)-1,knife_scores[-1],str(knife_scores[-1]))
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
    