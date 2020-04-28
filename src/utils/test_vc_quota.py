#!/usr/bin/env python3

import unittest
import logging
import logging.config
import itertools
import vc_quota

from cluster_resource import ClusterResource

log = logging.getLogger(__name__)


class TestVCQuota(unittest.TestCase):
    """
    Test quota.py
    """
    def test_adequate_quota(self):
        meta_full = {'cpu': {'Standard_ND40rs_v2': {
                                'per_node': 40, 'schedulable_ratio': 0.95},
                            'Standard_B2s': {
                                'per_node': 2, 'schedulable_ratio': 0.95}}, 
            'gpu': {'Standard_ND40rs_v2': {
                        'gpu_type': 'V100', 'per_node': 8}, 
                    'Standard_B2s': {'gpu_type': None, 'per_node': 0}}, 
            'gpu_memory': {'Standard_ND40rs_v2': {'per_node': '256Gi'}, 
                           'Standard_B2s': {'per_node': '0Gi'}}, 
            'memory': {'Standard_ND40rs_v2': {
                            'per_node': '672Gi', 'schedulable_ratio': 0.95}, 
                        'Standard_B2s': {
                            'per_node': '200Gi', 'schedulable_ratio': 0.95}}}
        
        meta_gpu_only = {'cpu': {'Standard_ND40rs_v2': {
                                'per_node': 40, 'schedulable_ratio': 0.95}}, 
            'gpu': {'Standard_ND40rs_v2': {
                        'gpu_type': 'V100', 'per_node': 8}}, 
            'gpu_memory': {'Standard_ND40rs_v2': {'per_node': '256Gi'}}, 
            'memory': {'Standard_ND40rs_v2': {
                            'per_node': '672Gi', 'schedulable_ratio': 0.95}}}
        
        meta_cpu_only = {'cpu': {'Standard_B2s': {
                                'per_node': 2, 'schedulable_ratio': 0.95}}, 
            'gpu': {'Standard_B2s': {'gpu_type': None, 'per_node': 0}}, 
            'gpu_memory': {'Standard_B2s': {'per_node': '0Gi'}}, 
            'memory': {'Standard_B2s': {
                            'per_node': '200Gi', 'schedulable_ratio': 0.95}}}
        
        worker_cnt_sku_full =  {'Standard_B2s': 3, 'Standard_ND40rs_v2': 160}
        
        worker_cnt_sku_gpu =  {'Standard_ND40rs_v2': 160}
        
        worker_cnt_sku_cpu = {'Standard_B2s': 3}

        plan_moderate = {'platform': {'gpu': {'Standard_ND40rs_v2': 32}, 
                                      'cpu': {'Standard_B2s': 1}}, 
                        'weather': {'cpu': {'Standard_ND40rs_v2': 40}, 
                                    'gpu': {'Standard_ND40rs_v2': 8}, 
                                    'gpu_memory': {'Standard_ND40rs_v2': '256Gi'}, 
                                    'memory': {'Standard_ND40rs_v2': '672Gi'}}}
    
        plan_gpu_plus = {'platform': {'gpu': {'Standard_ND40rs_v2': 3200}, 
                                      'cpu': {'Standard_B2s': 1}}, 
                        'weather': {'cpu': {'Standard_ND40rs_v2': 40}, 
                                    'gpu': {'Standard_ND40rs_v2': 8}, 
                                    'gpu_memory': {'Standard_ND40rs_v2': '256Gi'}, 
                                    'memory': {'Standard_ND40rs_v2': '672Gi'}}}

        plan_cpu_plus =  {'platform': {'gpu': {'Standard_ND40rs_v2': 32}, 
                                      'cpu': {'Standard_B2s': 1000}}, 
                        'weather': {'cpu': {'Standard_ND40rs_v2': 40}, 
                                    'gpu': {'Standard_ND40rs_v2': 8}, 
                                    'gpu_memory': {'Standard_ND40rs_v2': '256Gi'}, 
                                    'memory': {'Standard_ND40rs_v2': '672Gi'}}}

        metas = [meta_full, meta_gpu_only, meta_cpu_only]
        sku_cnts = [worker_cnt_sku_full, worker_cnt_sku_gpu, worker_cnt_sku_cpu]
        plans = [plan_moderate, plan_gpu_plus, plan_cpu_plus]

        params_ls = list(itertools.product(plans, metas, sku_cnts))
        target_ls = [True] + [False] * (len(params_ls) - 1)
        for params, target in zip(params_ls, target_ls):
            self.assertEqual(vc_quota.adequate_quota(*params), target)

   
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                        level=logging.INFO)
    unittest.main()
