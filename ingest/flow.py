from prefect import flow, task

@task
def step1_ingest():
    return "ingested"

@task
def step2_parse(data):
    return f"parsed {data}"

@task
def step3_thread(data):
    return f"threaded {data}"

@task
def step4_dedupe(data):
    return f"deduped {data}"

@task
def step5_store(data):
    return f"stored {data}"

@task
def step6_cluster(data):
    return "clusters"

@task
def step7_ner(data):
    return "entities"

@task
def step8_timeline(data):
    return "timeline"

@task
def step9_log(data):
    print("flow completed")
    return True

@flow
def ingest_flow():
    data = step1_ingest()
    data = step2_parse(data)
    data = step3_thread(data)
    data = step4_dedupe(data)
    data = step5_store(data)
    step6_cluster(data)
    step7_ner(data)
    step8_timeline(data)
    step9_log(data)

if __name__ == "__main__":
    ingest_flow()

    return list(dict.fromkeys(items))
