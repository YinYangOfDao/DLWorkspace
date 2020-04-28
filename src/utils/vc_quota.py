#!/usr/bin/env python3
import json
from collections import Counter
from cluster_resource import ClusterResource
from ConfigUtils import merge_config

def vc_value_str(config, ratio_dict):
    if "worker_sku_cnt" not in config or "sku_mapping" not in config:
        print(
            "Warning: no default value would be added to VC table. Need to manually specify"
        )
        return "", "", [], ""

    worker_sku_cnt, sku_mapping = config["worker_sku_cnt"], config[
        "sku_mapping"]
    quota_dict = {}
    old_meta = {}
    resource_quota = {"cpu": {}, "memory": {}, "gpu": {}, "gpu_memory": {}}
    for sku, cnt in worker_sku_cnt.items():
        gpu_type = sku_mapping.get(sku, {}).get("gpu-type", "None")
        num_gpu_per_node = sku_mapping.get(sku, {}).get("gpu", 0)
        quota_dict[gpu_type] = quota_dict.get(gpu_type,
                                              0) + cnt * num_gpu_per_node
        old_meta[gpu_type] = {"num_gpu_per_node": num_gpu_per_node}
        sku_name_in_map = sku if sku in sku_mapping else ""
        meta_tmp = sku_mapping.get(sku_name_in_map, {})
        for r_type in resource_quota.keys():
            resource_quota[r_type][
                sku_name_in_map] = resource_quota[r_type].get(
                    sku_name_in_map, 0) + meta_tmp.get(r_type, 0) * cnt

    for r_type in ["cpu", "memory"]:
        for sku, val in resource_quota[r_type].items():
            resource_quota[r_type][sku] *= config.get("schedulable_ratio", 0.9)

    # default value of quota and metadata are based on the assumption that there's only one default VC, this is not reasonable, and
    # these 2 fields would also finally get removed
    quota = json.dumps(quota_dict, separators=(",", ":"))
    metadata = json.dumps(old_meta, separators=(",", ":"))

    # TODO use cluster_resource.py to simplify code:
    # res_obj = ClusterResource(resource_quota), and directly multiply the ratio.
    res_quota = {}
    for vc, ratio in ratio_dict.items():
        res_quota_dict = {}
        for res, res_q in resource_quota.items():
            tmp_res_quota = {}
            for sku, cnt in res_q.items():
                cnt_p = cnt * ratio
                if "memory" in res:
                    cnt_p = '{}Gi'.format(cnt)
                tmp_res_quota[sku] = cnt_p
            res_quota_dict[res] = tmp_res_quota
        res_quota[vc] = json.dumps(res_quota_dict, separators=(",", ":"))

    res_meta_dict = {}
    for r_type in ["cpu", "memory", "gpu", "gpu_memory"]:
        tmp_res_meta = {}
        for sku in worker_sku_cnt:
            sku_name_in_map = sku if sku in sku_mapping else ""
            pernode_cnt = sku_mapping.get(sku_name_in_map, {}).get(r_type, 0)
            if "memory" in r_type:
                pernode_cnt = '{}Gi'.format(pernode_cnt)
            tmp_res_meta[sku_name_in_map] = {"per_node": pernode_cnt}
            if r_type in ["cpu", "memory"]:
                tmp_res_meta[sku_name_in_map]["schedulable_ratio"] = 0.9
            if r_type == "gpu":
                tmp_res_meta[sku_name_in_map]["gpu_type"] = sku_mapping.get(
                    sku_name_in_map, {}).get("gpu-type", "None")
        res_meta_dict[r_type] = tmp_res_meta
    res_meta = json.dumps(res_meta_dict, separators=(",", ":"))
    return quota, metadata, res_quota, res_meta


def categorize_quota_request_by_type(plan, meta):
    plan_gpu_quota, plan_cpu_quota = Counter(), Counter()
    for vc_req in plan.values():
        if "gpu" in vc_req:
            plan_gpu_quota += Counter(vc_req["gpu"])
        if "cpu" in vc_req:
            plan_cpu_quota += Counter(vc_req["cpu"])
    # gpu sku would also bring cpu to resourceQuota, but they shouldn't
    # count as "request", cpu request are those 
    # make sure no gpu sku is used to request cpu quota
    for sku, sku_spec in meta["gpu"].items():
        per_node = sku_spec["per_node"]
        gpu_type = sku_spec["gpu_type"]
        if per_node == 0 and gpu_type is None:
            plan_gpu_quota.pop(sku, None)
        else:
            plan_cpu_quota.pop(sku, None)
    return plan_gpu_quota, plan_cpu_quota


def adequate_quota(plan, meta, worker_sku_cnt):
    try:
        plan_gpu_quota, plan_cpu_quota = categorize_quota_request_by_type(
                                                        plan, meta)
        # check demand < total quota
        for r_type in ["gpu", "cpu"]:
            plan_quota = eval(f"plan_{r_type}_quota")
            for sku in plan_quota:
                per_node = meta[r_type].get(sku, {}).get("per_node", 0)
                sku_total = per_node * worker_sku_cnt.get(
                            sku, 0)
                if plan_quota[sku] > sku_total:
                    print(f"inadequate total quota of sku {sku}, "\
                        f"{plan_quota[sku]}/{sku_total} desired")
                    return False
        return True
    except:
        print("Error happened. Please check quota plan, resourceMetadata"\
            " and worker_sku_cnt")
        return False


def get_vc_row_by_gpu(quota_in_gpu, meta, worker_sku_cnt):
    """should not discount here, since the number in quota_in_gpu 
        might have already been discounted"""
    try:
        res_quota = {"gpu": {}, "cpu": {}, "memory": {}, "gpu_memory": {}}
        old_quota = {}
        old_meta = {}
        for sku, gpu_num in quota_in_gpu.items():
            sku_gpu_type = meta["gpu"][sku]["gpu_type"]
            old_quota[sku_gpu_type] = old_quota.get(
                                    sku_gpu_type, 0) + gpu_num
            old_meta[sku_gpu_type] = {"num_gpu_per_node": meta[
                                                    "gpu"][sku]["per_node"]}
            sku_dict = {ky: {sku: meta[ky][sku]["per_node"]} for \
                    ky in res_quota}
            sku_res = ClusterResource(sku_dict)
            sku_obj = sku_res * gpu_num / sku_dict["gpu"][sku]
            sku_dict = sku_obj.to_dict()
            merge_config(res_quota, sku_dict)
        return old_quota, old_meta, res_quota
    except:
        print("Error happened. Please check gpu quota request, "\
            "resourceMetadata and worker_sku_cnt")
        return False


def get_vc_row_by_cpu(quota_in_cpu, meta, worker_sku_cnt):
    """should not discount here, since the number in quota_in_gpu 
        might have already been discounted"""
    try:
        res_quota = {"gpu": {}, "cpu": {}, "memory": {}, "gpu_memory": {}}
        old_quota = {}
        old_meta = {}
        for sku, cpu_num in quota_in_cpu.items():
            sku_dict = {ky: {sku: meta[ky][sku]["per_node"]} for \
                    ky in res_quota}
            sku_res = ClusterResource(sku_dict)
            sku_obj = sku_res * cpu_num / sku_dict["cpu"][sku]
            sku_dict = sku_obj.to_dict()
            merge_config(res_quota, sku_dict)
        return res_quota
    except:
        print("Error happened. Please check gpu quota request, "\
            "resourceMetadata and worker_sku_cnt")
        return False


def compute_all_resource_by_gpu_or_cpu(plan, meta, worker_sku_cnt):
    """
    compute all resource based on input gpu or cpu count, e.g.
    {"gpu": {"Standard_ND40rs_v2": 32}, "cpu": {"Standard_B2s": 160}}
    """
    plan_gpu_quota, plan_cpu_quota = categorize_quota_request_by_type(
                                                    plan, meta)
    plan_rows = {}
    for vc, quota_req in plan.items():
        gpu_req = {sku: amount for sku, amount in quota_req.get(
                    "gpu", {}).items() if sku in plan_gpu_quota}
        cpu_req = {sku: amount for sku, amount in quota_req.get(
                    "cpu", {}).items() if sku in plan_cpu_quota}
        old_quota, old_meta, res_gpu_quota = get_vc_row_by_gpu(
                                gpu_req, meta, worker_sku_cnt)
        res_cpu_quota = get_vc_row_by_cpu(cpu_req, meta, worker_sku_cnt)
        merge_config(res_gpu_quota, res_cpu_quota)
        vc_row = {"quota": json.dumps(old_quota), "meta": json.dumps(old_meta), 
          "res_quota": json.dumps(res_gpu_quota), "res_meta": json.dumps(meta)}
        plan_rows[vc] = vc_row
    return plan_rows