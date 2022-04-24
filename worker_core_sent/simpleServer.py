import os
from util.aredis_queue import QueueRespondsTask
import asyncio
import logging
from util import Job
from util.sentenceTool import sent_cut, is_important_word







async def main():
    async def __main_task__(job_obj: Job, QRTask):
        job_obj.content["sent_summary"] = []
        for s in job_obj.content["texts"]:
            words = sent_cut(s)
            re_words= []
            for w in words:
                important_words = is_important_word(w)
                if len(important_words)==0:
                    continue
                re_words.extend(important_words)

            job_obj.content["sent_summary"].append(re_words)
        #
        await QRTask.to_master(job_obj.to_json(), job_obj.request_id)


    QRTask1 = QueueRespondsTask(task_name)
    while True:
        logging.warning("get work....")
        task = await QRTask1.get_content()
        logging.warning(f"get QRTask1:({task_name}) work -> {task}")
        if task is not None:
            #
            obj = task.get("obj", None)
            request_id = task.get("request_id", None)
            job_obj = Job(request_id=request_id, content=obj)

            #
            await __main_task__(job_obj, QRTask1)


        #
        await asyncio.sleep(1)


task_name = os.getenv("task_name", "core_sent")
asyncio.run(main())
