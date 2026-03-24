#!/usr/bin/env python

# Licensed under the MIT License.
# Copyright (c) Microsoft Corporation.

import sys
import os
from pathlib import Path

# Try to import as a package first (for when installed with pip)
try:
    from batteryml.preprocess import (
        DOWNLOAD_LINKS, download_file, SUPPORTED_SOURCES
    )
    from batteryml.pipeline import Pipeline
    from batteryml.builders import PREPROCESSORS
except ImportError:
    # If that fails, add the parent directory to sys.path
    current_dir = Path(__file__).resolve().parent
    parent_dir = current_dir.parent
    sys.path.append(str(parent_dir))
    
    # Now try to import from the actual modules
    from batteryml.preprocess import (
        DOWNLOAD_LINKS, download_file, SUPPORTED_SOURCES
    )
    from batteryml.pipeline import Pipeline
    from batteryml.builders import PREPROCESSORS

import mlflow
import argparse

def main():
    parser = argparse.ArgumentParser('BatteryML command line utilities.')
    subparsers = parser.add_subparsers()

    # download command
    download_parser = subparsers.add_parser(
        "download", help="Download raw files for public datasets")
    download_parser.add_argument(
        "dataset", choices=list(DOWNLOAD_LINKS.keys()),
        help="Public dataset to download")
    download_parser.add_argument(
        "output_dir", help="Directory to save the raw data files")
    download_parser.set_defaults(func=download)

    # preprocess command
    preprocess_parser = subparsers.add_parser(
        "preprocess",
        help="Organize the raw data files into BatteryData and save to disk")
    preprocess_parser.add_argument(
        "input_type", choices=[value for values in SUPPORTED_SOURCES.values() for value in values],
        help="Type of input raw files. For public datasets, specific "
             "preprocessor will be called. For standard battery test "
             "output files, the corresponding preprocessing logic "
             "will be applied.")
    preprocess_parser.add_argument(
        "--config", default="None",
        help="Path to the config file of Cycler.")
    preprocess_parser.add_argument(
        "raw_dir", help="Directory of raw input files.")
    preprocess_parser.add_argument(
        "output_dir", help="Directory to save the BatteryData files.")
    preprocess_parser.add_argument(
        "-q", "--quiet", "--silent", dest="silent",
        action="store_true", help="Suppress logs during preprocessing.")
    preprocess_parser.set_defaults(func=preprocess)

    # run command
    run_parser = subparsers.add_parser(
        "run", help="Run the given config for training or evaluation")
    run_parser.add_argument(
        "config", help="Path to the config file")
    run_parser.add_argument(
        "--workspace", type=str, default=None, help="Directory to save the checkpoints and predictions.")
    run_parser.add_argument(
        "--device", default="cpu", help="Running device")
    run_parser.add_argument(
        "--ckpt-to-resume", "--ckpt_to_resume", dest="ckpt_to_resume",
        help="path to the checkpoint to resume training or evaluation")
    run_parser.add_argument(
        "--train", action="store_true",
        help="Run training. Will skip training if this flag is not provided.")
    run_parser.add_argument(
        "--eval", action="store_true",
        help="Run evaluation. Will skip eval if this flag is not provided.")
    run_parser.add_argument(
        "--metric", default="RMSE,MAE,MAPE",
        help="Metrics for evaluation, seperated by comma")
    run_parser.add_argument(
        "--seed", type=int, default=0, help="random seed")
    run_parser.add_argument(
        "--epochs", type=int, help="number of epochs override")
    run_parser.add_argument(
        "--skip_if_executed", type=str, default='False', help="skip train/evaluate if the model executed")
    run_parser.set_defaults(func=run)

    args = parser.parse_args()

    # ✅ If no subcommand provided → default to "run"
    if not hasattr(args, "func"):
        print("⚠️ No command provided. Defaulting to 'run' with preset arguments.")

        # Build default args
        default_args = argparse.Namespace(
            func=run,
            config="configs/baselines/sklearn/variance_model/matr_1.yaml",
            workspace="./workspace",
            device="cpu",
            ckpt_to_resume=None,
            train=True,
            eval=True,
            metric="RMSE,MAE,MAPE",
            seed=0,
            epochs=None,
            skip_if_executed=False
        )
        args = default_args

    args.func(args)


def download(args):
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    raw_dir = Path(args.output_dir)
    for f in DOWNLOAD_LINKS[args.dataset]:
        if len(f) == 2:
            (url, filename), total_length = f, None
        else:
            url, filename, total_length = f
        download_file(url, raw_dir / filename, total_length=total_length)


def preprocess(args):
    assert os.path.exists(
        args.raw_dir), f'Input path not exist: {args.raw_dir}'
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    config_path = Path(args.config)
    input_path, output_path = Path(args.raw_dir), Path(args.output_dir)
    processor = PREPROCESSORS.build(dict(
        name=f'{args.input_type}Preprocessor',
        output_dir=output_path,
        silent=args.silent
    ))
    processor(input_path, config_path=config_path)

def log_model_auto(model, artifact_path="model"):
    if model is None:
        return

    # Extract core model from BatteryML wrapper if present
    core_model = model
    if hasattr(model, 'model') and model.model is not None:
        core_model = model.model

    # --- sklearn ---
    try:
        import sklearn.base
        if isinstance(core_model, sklearn.base.BaseEstimator):
            import mlflow.sklearn
            mlflow.sklearn.log_model(core_model, artifact_path)
            return
    except Exception: pass

    # --- PyTorch ---
    try:
        import torch.nn as nn
        if isinstance(core_model, nn.Module):
            import mlflow.pytorch
            mlflow.pytorch.log_model(core_model, artifact_path)
            return
    except Exception: pass

    # --- Fallback to PyFunc ---
    import mlflow.pyfunc
    class GenericWrapper(mlflow.pyfunc.PythonModel):
        def __init__(self, m): self.m = m
        def predict(self, context, model_input): return self.m.predict(model_input)

    mlflow.pyfunc.log_model(artifact_path=artifact_path, python_model=GenericWrapper(model))

def run(args):
    # --- Load .env automatically ---
    env_path = Path(".env")
    if env_path.exists():
        with env_path.open() as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value

    # Ensure MLflow environment variables are present
    mlflow_tracking_uri = os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db")
    mlflow.set_tracking_uri(mlflow_tracking_uri)
    mlflow.enable_system_metrics_logging()
    mlflow.set_experiment("BatteryML")

    # Convert skip_if_executed to boolean
    args.skip_if_executed = str(args.skip_if_executed).lower() in ['true', '1', 'yes']

    pipeline = Pipeline(args.config, args.workspace)
    model, dataset = None, None

    with mlflow.start_run() as run_context:
        run_id = run_context.info.run_id
        
        # ✅ UNIQUE WORKSPACE GENERATION
        # Append the MLflow run_id to the workspace so every run is isolated
        base_workspace = Path(args.workspace or "./workspaces/default")
        args.workspace = str(base_workspace / run_id)
        os.makedirs(args.workspace, exist_ok=True)
        
        print(f"🏃 Running MLflow run ID: {run_id}")
        print(f"📂 Workspace for this run: {args.workspace}")

        pipeline = Pipeline(args.config, args.workspace)
        model, dataset = None, None

        if args.train:
            model, dataset = pipeline.train(
                seed=args.seed,
                device=args.device,
                epochs=args.epochs,
                ckpt_to_resume=args.ckpt_to_resume
            )
            log_model_auto(model)

        if args.eval:
            results = pipeline.evaluate(
                seed=args.seed,
                device=args.device,
                metric=args.metric.split(','),
                model=model,
                dataset=dataset,
                ckpt_to_resume=args.ckpt_to_resume,
                skip_if_executed=args.skip_if_executed
            )

            if results and isinstance(results, dict):
                clean_metrics = {}
                for k, v in results.items():
                    try:
                        val = v.item() if hasattr(v, 'item') else v
                        clean_metrics[str(k)] = float(val)
                    except Exception:
                        continue
                if clean_metrics:
                    mlflow.log_metrics(clean_metrics)

        # Log artifacts from the specific workspace created for this run
        workspace_dir = Path(args.workspace)
        if workspace_dir.exists():
            mlflow.log_artifacts(str(workspace_dir), artifact_path="workspace_files")

    print(f"✅ Run complete! View at: {os.environ.get('MLFLOW_HOST', 'localhost')}:{os.environ.get('MLFLOW_PORT', '5000')}")

if __name__ == "__main__":
    main()