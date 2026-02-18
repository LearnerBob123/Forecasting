import lightning.pytorch as pl
from lightning.pytorch.tuner import Tuner


def run_lr_finder(model, train_loader, val_loader):

    trainer = pl.Trainer(max_epochs=1)
    tuner = Tuner(trainer)

    lr_finder = tuner.lr_find(
        model,
        train_dataloaders=train_loader,
        val_dataloaders=val_loader
    )

    suggested_lr = lr_finder.suggestion()

    print(f"\nSuggested Learning Rate: {suggested_lr}\n")

    return suggested_lr
