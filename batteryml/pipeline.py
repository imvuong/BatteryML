# Licensed under the MIT License.
# Copyright (c) Microsoft Corporation.

from __future__ import annotations

import os
import torch
import pickle
import random
import shutil
import hashlib
import numpy as np

from pathlib import Path
from datetime import datetime

from batteryml.task import Task
from batteryml.data import DataBundle
from batteryml.builders import MODELS
from batteryml.utils import import_config
from batteryml.models.base import BaseModel


class Pipeline:
    """
    Main class for managing the machine learning pipeline for battery-related tasks.
    Handles configuration, training, and evaluation of models.
    """
    def __init__(self, config_path: Path | str, workspace: Path | str):
        """
        Initialize the Pipeline with a configuration file and workspace.

        :param config_path: Path to the configuration file
        :param workspace: Path to the workspace directory
        """
        self.config_path = config_path
        self.config = load_config(config_path, workspace)

    def train(self,
              seed: int = 0,
              epochs: int | None = None,
              device: torch.device | str = 'cpu',
              ckpt_to_resume: str | None = None,
              skip_if_executed: bool = True,
              dataset: DataBundle | None = None):
        """
        Train the model based on the configuration.

        :param seed: Random seed for reproducibility
        :param epochs: Number of epochs to train (overrides config if provided)
        :param device: Device to run the training on (e.g., 'cpu' or 'cuda')
        :param ckpt_to_resume: Path to a checkpoint to resume training from
        :param skip_if_executed: Whether to skip training if a checkpoint already exists
        :param dataset: Pre-built dataset (if None, will be built from config)
        :return: Trained model and dataset
        """
        set_seed(seed)

        # Skip training if a checkpoint already exists and skip_if_executed is True
        if skip_if_executed and (
            self.config['workspace'] is not None
            and any(Path(self.config['workspace'])
                    .glob(f'*seed_{seed}_*.ckpt'))
        ):
            # TODO: maybe we should add a logging util for handling infos
            print(f'Skip training for {self.config["workspace"]} '
                  'as the checkpoint already exists.')
            return

        # Prepare dataset if not provided
        if dataset is None:
            dataset, raw_data = build_dataset(self.config, device)
            self.raw_data = raw_data

        # Override number of epochs if provided
        if epochs is not None:
            original_epochs = self.config['model'].get('epochs')
            self.config['model']['epochs'] = epochs

        # Prepare and train the model
        model = self._prepare_model(ckpt_to_resume, device)
        ts = timestamp()

        # Save a copy of the config in the workspace
        if model.workspace is not None:
            shutil.copyfile(
                self.config_path,
                model.workspace / f'config_{ts}.yaml')

        model.fit(dataset, timestamp=ts)

        # Restore the original epochs in config
        if epochs is not None:
            self.config['model']['epochs'] = original_epochs


        return model, dataset

    def evaluate(self,
                 seed: int = 0,
                 device: torch.device | str = 'cpu',
                 metric: list | str = 'RMSE',
                 model: BaseModel | None = None,
                 dataset: DataBundle | None = None,
                 ckpt_to_resume: str | None = None,
                 skip_if_executed: bool = True):
        """
        Evaluate the model based on the configuration.

        :param seed: Random seed for reproducibility
        :param device: Device to run the evaluation on
        :param metric: Metric(s) to use for evaluation
        :param model: Pre-built model (if None, will be built from config)
        :param dataset: Pre-built dataset (if None, will be built from config)
        :param ckpt_to_resume: Path to a checkpoint to resume from
        :param skip_if_executed: Whether to skip evaluation if predictions already exist
        :return: Evaluation scores
        """
        set_seed(seed)

        # Skip evaluation if predictions already exist and skip_if_executed is True
        if skip_if_executed and (
            self.config['workspace'] is not None
            and any(Path(self.config['workspace'])
                    .glob(f'predictions_seed_{seed}_*.pkl'))
        ):
            print(f'Skip evaluation for {self.config["workspace"]} '
                  'as the prediction exists.')
            return

        # Prepare dataset and model if not provided
        if dataset is None:
            dataset, raw_data = build_dataset(self.config, device)
            self.raw_data = raw_data
        if model is None:
            model = self._prepare_model(ckpt_to_resume, device)

        # Make predictions and calculate scores
        prediction = model.predict(dataset)

        if isinstance(metric, str):
            metric = [metric]

        scores = {
            m: dataset.evaluate(prediction, m) for m in metric
        }
        print(scores)
        ts = timestamp()

        # Save predictions and scores if workspace is specified
        if self.config['workspace'] is not None:
            obj = {
                'prediction': prediction,
                'scores': scores,
                'data': dataset.to('cpu'),
                'seed': seed,
            }
            filename = f'predictions_seed_{seed}_{ts}.pkl'
            with open(Path(self.config['workspace']) / filename, 'wb') as f:
                pickle.dump(obj, f)
                
        return scores

    def _prepare_model(self,
                       ckpt_to_resume: str | None = None,
                       device: torch.device | None = 'cpu'
                       ) -> BaseModel:
        """
        Prepare the model for training or evaluation.

        :param ckpt_to_resume: Path to a checkpoint to resume from
        :param device: Device to load the model on
        :return: Prepared model
        """
        model = MODELS.build(self.config['model'])
        if model.workspace is None:
            model.workspace = self.config['workspace']
        if ckpt_to_resume is not None:
            model.load_checkpoint(ckpt_to_resume)

        # Use torch.compile for PyTorch 2.0+ and if model is a torch.nn.Module
        if torch.__version__ >= '2' and isinstance(model, torch.nn.Module):
            model = torch.compile(model)

        model = model.to(device)
        return model

# List of configuration fields to be loaded
CONFIG_FIELDS = [
    'model',
    'train_test_split',
    'feature',
    'label',
    'feature_transformation',
    'label_transformation'
]


def load_config(config_path: str,
                workspace: str | None,
                config_fields: list | None = None
                ) -> dict:
    """
    Load and process the configuration file.

    :param config_path: Path to the configuration file
    :param workspace: Path to the workspace directory
    :param config_fields: List of configuration fields to load
    :return: Processed configuration dictionary
    """
    config_path = Path(config_path)
    config_fields = config_fields or CONFIG_FIELDS
    configs = import_config(config_path, config_fields)

    # Determine the workspace path
    if configs['model'].get('workspace') is not None:
        workspace = Path(configs['model'].get('workspace'))
    elif workspace is not None:
        if workspace.strip().lower() == 'none':
            workspace = None
        else:
            workspace = Path(workspace)
    else:
        workspace = Path.cwd() / 'workspaces' / config_path.relative_to('configs').with_suffix('')  

    if workspace is not None and workspace.exists():
        assert workspace.is_dir(), workspace

    if workspace is not None and not workspace.exists():
        os.makedirs(workspace)

    configs['workspace'] = workspace
    print(workspace)
    return configs


def build_dataset(configs: dict,
                  device: str,
                  config_fields: list | None = None):
    """
    Build or load the dataset based on the configuration.

    :param configs: Configuration dictionary
    :param device: Device to load the dataset on
    :param config_fields: List of configuration fields to use for caching
    :return: Tuple of (dataset, raw_data)
    """
    strings = []
    config_fields = config_fields or CONFIG_FIELDS[1:]
    for field in config_fields:
        strings.append(recursive_dump_string(configs[field]))
    filename = hash_string('+'.join(strings))
    cache_dir = Path('cache')
    if not cache_dir.exists():
        cache_dir.mkdir()
    cache_file = Path(cache_dir / f'battery_cache_{filename}.pkl')

    # Load from cache if it exists
    if cache_file.exists():
        print(f'Load datasets from cache {str(cache_file)}.')
        with open(cache_file, 'rb') as f:
            data = pickle.load(f)
            dataset = data['dataset']
            raw_data = data['raw_data']
    else:
        # Build the dataset if not in cache
        task = Task(
            label_annotator=configs['label'],
            feature_extractor=configs['feature'],
            train_test_splitter=configs['train_test_split'],
            feature_transformation=configs['feature_transformation'],
            label_transformation=configs['label_transformation'])

        dataset = task.build()
        train_cells, test_cells = task.get_raw_data()
        data = {'dataset':dataset,
                'raw_data':{
                    'train_cells': train_cells,
                    'test_cells': test_cells,
                }}
        raw_data = data['raw_data']
        # store cache
        with open(cache_file, 'wb') as f:
            pickle.dump(data, f)

    return dataset.to(device), raw_data


def set_seed(seed: int):
    """
    Set random seed for reproducibility across multiple libraries.

    :param seed: Seed value to set
    """
    print(f'Seed is set to {seed}.')
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True


def recursive_dump_string(data):
    """
    Recursively convert nested data structures to a string representation.

    :param data: Data to convert (can be list, dict, or other types)
    :return: String representation of the data
    """
    if isinstance(data, list):
        return '_'.join([recursive_dump_string(x) for x in data])
    if isinstance(data, dict):
        return '_'.join([
            recursive_dump_string(data[key])
            for key in sorted(data.keys())
        ])
    return str(data)


def hash_string(string):
    """
    Create a truncated hash of a string.

    :param string: String to hash
    :return: Truncated hash string
    """
    sha256_hash = hashlib.sha256()
    sha256_hash.update(string.encode('utf-8'))
    hash_value = sha256_hash.hexdigest()
    truncated_hash = hash_value[:32]
    return truncated_hash


def timestamp(marker: bool = False):
    """
    Generate a timestamp string.

    :param marker: If True, use a format with spaces and colons
    :return: Timestamp string
    """
    template = '%Y-%m-%d %H:%M:%S' if marker else '%Y%m%d%H%M%S'
    return datetime.now().strftime(template)


