default_az_parameters = {
    "azure_cluster": {
        "subscription": "Bing DLTS",
        "infra_node_num": 1, 
        "worker_node_num": 2,
        "mysqlserver_node_num": 0,
        "elasticsearch_node_num": 0,
        "nfs_node_num": 1,
        "azure_location": "westus2",
        "infra_vm_size": "Standard_D1_v2",
        "worker_vm_size": "Standard_NC6",
        "mysqlserver_vm_size": "Standard_D1_v2",
        "elasticsearch_vm_size": "Standard_D1_v2",
        "nfs_vm_size": "Standard_D1_v2",
        "vm_image": "Canonical:UbuntuServer:18.04-LTS:18.04.201912180",
        "os_storage_sku": "Premium_LRS",
        "os_storage_sz": 64,
        "vm_local_storage_sku": "Premium_LRS",
        "infra_local_storage_sz": 1024,
        "worker_local_storage_sz": 1024,
        "mysqlserver_local_storage_sz": 2048,
        "elasticsearch_local_storage_sz" : 2048,
        "lustre_local_storage_sz" : 1024,
        "nfs_data_disk_sku": "Premium_LRS",
        "nfs_data_disk_sz": 1024,
        "nfs_data_disk_num": 1,
        "nfs_data_disk_path": '/data',
        "nfs_vm": [],
        "eviction_policy": "Deallocate",
        "single_placement_group": "false",
        "default_low_priority_domain": "redmond.corp.microsoft.com",
    },
    "sku_mapping": {
        'Standard_NC6s_v2': {'cpu': 6, 'memory': 112, 'gpu': 1, 'gpu_memory': 16, 'gpu-type': 'P100'}, 
        'Standard_NC12s_v2': {'cpu': 12, 'memory': 224, 'gpu': 2, 'gpu_memory': 32, 'gpu-type': 'P100'}, 
        'Standard_NC24s_v2': {'cpu': 24, 'memory': 448, 'gpu': 4, 'gpu_memory': 64, 'gpu-type': 'P100'}, 
        'Standard_NC6s_v3': {'cpu': 6, 'memory': 112, 'gpu': 1, 'gpu_memory': 16, 'gpu-type': 'V100'}, 
        'Standard_NC12s_v3': {'cpu': 12, 'memory': 224, 'gpu': 2, 'gpu_memory': 32, 'gpu-type': 'V100'}, 
        'Standard_NC24s_v3': {'cpu': 24, 'memory': 448, 'gpu': 4, 'gpu_memory': 64, 'gpu-type': 'V100'}, 
        'Standard_ND6s': {'cpu': 6, 'memory': 112, 'gpu': 1, 'gpu_memory': 24, 'gpu-type': 'P40'}, 
        'Standard_ND12s': {'cpu': 12, 'memory': 224, 'gpu': 2, 'gpu_memory': 48, 'gpu-type': 'P40'}, 
        'Standard_ND24s': {'cpu': 24, 'memory': 448, 'gpu': 4, 'gpu_memory': 96, 'gpu-type': 'P40'},
        'Standard_ND40s_v2': {'cpu': 40, 'memory': 672, 'gpu': 8, 'gpu_memory': 128, 'gpu-type': 'V100'},
        'Standard_ND40rs_v2': {'cpu': 40, 'memory': 672, 'gpu': 8, 'gpu_memory': 256, 'gpu-type': 'V100', 'IB': True},
        'Standard_NV6': {'cpu': 6, 'memory': 56, 'gpu': 1, 'gpu_memory': 8, 'gpu-type': 'M60'}, 
        'Standard_NV12': {'cpu': 12, 'memory': 112, 'gpu': 2, 'gpu_memory': 16, 'gpu-type': 'M60'}, 
        'Standard_NV24': {'cpu': 24, 'memory': 224, 'gpu': 4, 'gpu_memory': 32, 'gpu-type': 'M60'}, 
        'Standard_NV12s_v3': {'cpu': 12, 'memory': 112, 'gpu': 1, 'gpu_memory': 8, 'gpu-type': 'M60'}, 
        'Standard_NV24s_v3': {'cpu': 24, 'memory': 224, 'gpu': 2, 'gpu_memory': 16, 'gpu-type': 'M60'}, 
        'Standard_NV48s_v3': {'cpu': 48, 'memory': 448, 'gpu': 4, 'gpu_memory': 32, 'gpu-type': 'M60'}, 
        'Standard_NC24rs_v2': {'cpu': 24, 'memory': 448, 'gpu': 4, 'gpu_memory': 64, 'gpu-type': 'P100', 'IB': True}, 
        'Standard_NC24rs_v3': {'cpu': 24, 'memory': 448, 'gpu': 4, 'gpu_memory': 64, 'gpu-type': 'V100', 'IB': True}, 
        'Standard_ND24rs': {'cpu': 24, 'memory': 448, 'gpu': 4, 'gpu_memory': 96, 'gpu-type': 'P40', 'IB': True},
        'Standard_B1ls1': {'cpu': 1, 'memory': 0.5}, 
        'Standard_B1s': {'cpu': 1, 'memory': 1.0}, 
        'Standard_B1ms': {'cpu': 1, 'memory': 2.0}, 
        'Standard_B2s': {'cpu': 2, 'memory': 4.0}, 
        'Standard_B2ms': {'cpu': 2, 'memory': 8.0}, 
        'Standard_B4ms': {'cpu': 4, 'memory': 16.0}, 
        'Standard_B8ms': {'cpu': 8, 'memory': 32.0}, 
        'Standard_B12ms': {'cpu': 12, 'memory': 48.0}, 
        'Standard_B16ms': {'cpu': 16, 'memory': 64.0}, 
        'Standard_B20ms': {'cpu': 20, 'memory': 80.0},
    }

}
