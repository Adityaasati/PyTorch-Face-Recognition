
from tqdm.auto import tqdm
from torch import nn
import torch
from typing import Tuple, Dict, List


def train_fn(model:torch.nn.Module,
             dataloader:torch.utils.data.DataLoader,
             loss_fn:torch.nn.Module,
             optimizer:torch.optim.Optimizer,
             device: torch.device) -> Tuple[float, float]:

  model.train()

  train_loss, train_acc =0,0


  for batch, (X,y) in enumerate(dataloader):

    X,y = X.to(device), y.to(device)

    y_pred = model(X)

    loss = loss_fn(y_pred, y)
    train_loss+=loss.item()

    optimizer.zero_grad()

    loss.backward()

    optimizer.step()

    y_pred_class = torch.argmax(torch.softmax(y_pred, dim=1), dim=1)
    train_acc += (y_pred_class == y).sum().item()/len(y_pred)

  train_loss = train_loss/len(dataloader)
  train_acc = train_acc/len(dataloader)
  return train_loss,train_acc

def test_fn(model:torch.nn.Module,
            dataloader: torch.utils.data.DataLoader,
            loss_fn:torch.nn.Module,
            device: torch.device) -> Tuple[float, float]:

  model.eval()
  test_loss, test_acc=0,0

  with torch.inference_mode():
    for batch, (X,y) in enumerate(dataloader):
      X,y = X.to(device),y.to(device)
      test_pred = model(X)

      loss = loss_fn(test_pred,y)
      test_loss+=loss.item()

      test_labels = test_pred.argmax(dim=1)
      test_acc += (test_labels == y).sum().item()/len(test_pred)

  test_loss = test_loss/len(dataloader)
  test_acc = test_acc/len(dataloader)

  return test_loss, test_acc




def train_and_test(model: torch.nn.Module,
          train_dataloader: torch.utils.data.DataLoader,
          test_dataloader: torch.utils.data.DataLoader,
          optimizer: torch.optim.Optimizer,
          loss_fn: torch.nn.Module,
          epochs: int,
          device: torch.device) -> Dict[str, List[float]]:

  results = {"train_acc":[],
             "train_loss":[],
             "test_acc":[],
             "test_loss":[]
             }
  for epoch in tqdm(range(epochs)):
    train_loss, train_acc  = train_fn(model=model,
                                    dataloader=train_dataloader,
                                    loss_fn=loss_fn,
                                    optimizer=optimizer,
                                      device=device)
    test_loss, test_acc  = test_fn(model=model,
                                    dataloader=test_dataloader,
                                    loss_fn=loss_fn,
                                    device=device)
    print(f"Epoch: {epoch} | Train Loss: {train_loss} | Train acc: {train_acc} | Test Loss: {test_loss} | Test acc: {test_acc}")
    results['train_acc'].append(train_acc)
    results['train_loss'].append(train_loss)
    results['test_acc'].append(test_acc)
    results['test_loss'].append(test_loss)

  return results



