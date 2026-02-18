import lightning.pytorch as pl
from lightning.pytorch.callbacks import EarlyStopping, ModelCheckpoint


def train_model(model, train_loader, val_loader, config):

    checkpoint_callback = ModelCheckpoint(
        monitor="val_loss",
        dirpath="checkpoints",
        filename="tft-best",
        save_top_k=1,
        mode="min"
    )

    early_stop = EarlyStopping(
        monitor="val_loss",
        patience=10,
        mode="min"
    )

    trainer = pl.Trainer(
        max_epochs=config["max_epochs"],
        accelerator="auto",
        devices=1,
        gradient_clip_val=0.1,
        callbacks=[early_stop, checkpoint_callback],
    )

#     trainer = pl.Trainer(
#     max_epochs=50,                   # Train for up to 50 epochs (early stop may end sooner)
#     accelerator="gpu",               # Use GPU (automatically falls back to CPU if unavailable)
#     devices=1,                       # Use 1 GPU (or "auto" to use all available)
#     enable_model_summary=True,       # Print model architecture at start
#     gradient_clip_val=0.1,           # Clip gradients to ||g|| <= 0.1 (prevents instability)
    
#     # Logging and checkpointing
#     callbacks=[lr_logger, early_stop_callback],
#     logger=logger,
    
#     # Progress bar
#     enable_progress_bar=True,
#     log_every_n_steps=10,            # Log metrics every 10 batches
    
#     # Precision and stability
#     precision="32-true",             # Use full 32-bit precision (vs mixed precision)
#     deterministic=False,             # Set True if you need reproducibility
    
#     # Debugging
#     detect_anomaly=False,            # Set True to detect NaN/Inf in gradients
    
#     # Comment out for production:
#     limit_train_batches=1.0,       # Use only 10% of data for quick testing
#     #  fast_dev_run=True,             # Run 1 batch per phase to check for bugs (very fast)
#     limit_val_batches = 1.0
# )

    trainer.fit(model, train_loader, val_loader)

    print(f"\nBest model saved at: {checkpoint_callback.best_model_path}\n")

    return trainer, checkpoint_callback.best_model_path
