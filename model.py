import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os
import datetime

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size) -> None:
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear4 = nn.Linear(hidden_size, output_size)

    def forward(self,x):
        x = F.relu(self.linear1(x))
        x = self.linear4(x)
        return x
    
    def save(self,file_name=None,score=None):
        folder_path="./model_saves"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        if not file_name:
            current_datetime = datetime.datetime.now()
            formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"model_score{score}_{formatted_datetime}"
        file_name+=".pth"
        file_name = os.path.join(folder_path,file_name)
        torch.save(self.state_dict(),file_name)
        if os.path.isfile(file_name):
            print(f"file saved as {file_name}")

    def load(self, file_path):
        if os.path.isfile(file_path):
            self.load_state_dict(torch.load(file_path))
            self.eval()
            print(f"Model loaded from {file_path}")
        else:
            print(f"File {file_path} does not exist")

class QTrainer:
    def __init__(self,model,lr,gamma) -> None:
        self.model=model
        self.lr=lr
        self.gamma=gamma
        self.optimizer=optim.Adam(model.parameters(),lr=self.lr)
        self.criterion=nn.MSELoss()

    def train_step(self,state,action,reward,next_state,done):
        state=torch.tensor(state,dtype=torch.float)
        action=torch.tensor(action,dtype=torch.float)
        reward=torch.tensor(reward,dtype=torch.float)
        next_state=torch.tensor(next_state,dtype=torch.float)
        # here we have (n,x)

        if len(state.shape) == 1:
            # here we transofrm to (1,x) for short memory case
            state=torch.unsqueeze(state,0)
            action=torch.unsqueeze(action,0)
            reward=torch.unsqueeze(reward,0)
            next_state=torch.unsqueeze(next_state,0)
            done=(done,)

        # step 1: Predicted Q:
        pred=self.model(state)

        # step 2: New Q= Reward + gamma * max(predicted Q value)
        target = pred.clone()

        for idx in range(len(done)):
            Q_new=reward[idx]
            if not done[idx]:
                Q_new=reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            target[idx][torch.argmax(action).item()]=Q_new

        self.optimizer.zero_grad()
        loss=self.criterion(target,pred)
        loss.backward()

        self.optimizer.step()