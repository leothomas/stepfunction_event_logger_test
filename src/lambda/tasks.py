
class FailedTask(Exception):
    pass

def handler_task_1(event, context):
    if "test_failure" in event: 
        raise FailedTask("Task 1 was purposefully failed :(")
    else: 
        return {"task1_output": "(With borat voice) Great Success from task 1!"}

def handler_task_2(event, context):
    if "test_failure" in event: 
        raise FailedTask("Task 2 was purposefully failed :(")
    else: 
        return {"task1_output": "(With borat voice) Great Success from task 2!"}
