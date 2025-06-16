config_dict = {
    # environment settings
    "gpu_id": 0,  # default: 0
    "worker": 0,  # default: 0
    "seed": 42,  # default: "2020"
    "state": "INFO",  # default: "INFO"
    "encoding": "utf-8",  # default: "utf-8"
    "reproducibility": True,  # default: True
    "data_path": "./data_sets/",  # default: "dataset/"
    "checkpoint_dir": "saved/",  # default: "saved/"
    "show_progress": True,  # default: True
    "save_dataset": False,  # default: False
    "dataset_save_path": None,  # default: None
    "save_dataloaders": False,  # default: False
    "dataloaders_save_path": None,  # default: None
    "log_wandb": False,  # default: False
    "wandb_project": "recbole",  # default: "recbole"
    "shuffle": True,  # default: True
    # data settings
    # atomic file format
    "field_separator": "\t",  # default: "\t"
    "seq_separator": " ",  # default: " "
    # basic information
    # common features
    "USER_ID_FIELD": "user_id",  # default: "user_id"
    "ITEM_ID_FIELD": "item_id",  # default: "item_id"
    "RATING_FIELD": "rating",  # default: "rating"
    "TIME_FIELD": "timestamp",  # default: "timestamp"
    "seq_len": {},  # default: {}
    # label for point-wise dataloader
    "LABEL_FIELD": "label",  # default: "label"
    "threshold": None,  # default: None
    # negative sampling prefix for pair-wise dataloader
    "NEG_PREFIX": "neg_",  # default: "neg_"
    # sequential model needed
    "ITEM_LIST_LENGTH_FIELD": "item_length",  # default: "item_length"
    "LIST_SUFFIX": "_list",  # default: "_list"
    "MAX_ITEM_LIST_LENGTH": 50,  # default: 50
    "POSITION_FIELD": "position_id",  # default: "position_id"
    # knowledge-based model needed
    "HEAD_ENTITY_ID_FIELD": "head_id",  # default: "head_id"
    "TAIL_ENTITY_ID_FIELD": "tail_id",  # default: "tail_id"
    "RELATION_ID_FIELD": "relation_id",  # default: "relation_id"
    "kg_reverse_r": False,  # default: False
    "entity_kg_num_interval": "[0, inf)",  # default: "[0, inf)"
    "relation_kg_num_interval": "[0, inf)",  # default: "[0, inf)"
    # selectively loading
    "load_col": {"inter": ["user_id", "item_id", "rating"]},  # default: {inter: [user_id, item_id]}
    "unload_col": {},  # default: {}
    "unused_col": {},  # default: {}
    "additional_feat_suffix": [],  # default: []
    "numerical_features": [],  # default: []
    # filtering
    # remove duplicated user-item interactions
    "rm_dup_inter": None,  # default: None
    # filter by value
    "val_interval": {},  # default: {}
    # remove interaction by user or item
    "filter_inter_by_user_or_item": True,  # default: True
    # filter by number of interactions
    "user_inter_num_interval": "[0, inf)",  # default: "[0, inf)"
    "item_inter_num_interval": "[0, inf)",  # default: "[0, inf)"
    # preprocessing
    "alias_of_user_id": None,  # default: None
    "alias_of_item_id": None,  # default: None
    "alias_of_entity_id": None,  # default: None
    "alias_of_relation_id": None,  # default: None
    "preload_weight": {},  # default: {}
    "normalize_field": [],  # default: []
    "normalize_all": False,  # default: False
    "discretization": None,  # default: None
    # benchmark file
    "benchmark_filename": ["train_0", "valid_0", "test_0"],  # default: None
    # training settings
    "epochs": 50,  # default: 300
    "train_batch_size": 2048,  # default: 2048
    "learner": "adam",  # default: "adam"
    "learning_rate": 0.001,  # default: 0.001
    "training_neg_sample_args":
        {
            "distribution": "uniform",  # default: "uniform"
            "sample_num": 1,  # default: 1
            "dynamic": False,  # default: False
            "candidate_num": 0,  # default: 0
        },
    "eval_step": 5,  # default: 1
    "stopping_step": 10,  # default: 10
    "clip_grad_norm": None,  # default: None
    "loss_decimal_place": 4,  # default: 4
    "weight_decay": 0.0,  # default: 0.0
    "require_pow": False,  # default: False
    "enable_amp": False,  # default: False
    "enable_scaler": False,  # default: False
    # evaluation settings
    "eval_args":
        {
            "group_by": "user",  # default: "user"
            "order": "RO",  # default: "RO"
            "split":
                {
                    # "RS": [8, 1, 1] # default: {"RS": [8, 1, 1]}
                    "LS": "valid_and_test"
                },
            "mode":
                {
                    "valid": "uni100",  # default: "full"
                    "test": "uni100",  # default: "full"
                },
        },
    "repeatable": False,  # default: False
    "metrics": ["Recall", "MRR", "NDCG", "Hit", "MAP", "Precision", "GAUC", "ItemCoverage", "AveragePopularity",
                "GiniIndex", "ShannonEntropy", "TailPercentage"],
    # default: ["Recall", "MRR", "NDCG", "Hit", "Precision"]
    "topk": [1, 3, 5, 10, 20],  # default: 10
    "valid_metric": "NDCG@10",  # default: "MRR@10"
    "eval_batch_size": 4096,  # default: 4096
    "metric_decimal_place": 4,  # default: 4,
    # misc settings
    "model": None,
    "MODEL_TYPE": None
}
