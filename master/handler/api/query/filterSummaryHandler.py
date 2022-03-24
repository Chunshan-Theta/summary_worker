import json

from handler.api.apiHandlerBase import APIHandlerBase
from util.aredis_queue import QueueRequestTask
import asyncio


class filterSummaryHandler(APIHandlerBase):

    async def post(self):
        """
        ---
        tags:
        - model
        summary: List posts
        description: List all posts in feed
        produces:
        - application/json
        parameters:
        -   in: body
            name: body
            description: post data
            required: true
            schema:
                type: object
                properties:

                    corpus:
                        type: array
                        items:
                            type: string
                        default: [
                            "如個案有居家服務需求該如何得知此個案預派案的輪序單位",
                            "A單位與案家討論完服務後需簽立同意書會有ㄧ致性的範本嗎",
                            "A單位人員完訓後須到照管中心實習於實習前組合包的內容是照專擬定該由誰協助處理",
                            "請問A級單位特約申請作業大概什麼時候會公告呢"
                        ]
        responses:
            200:
              description: test
        """
        body = json.loads(self.request.body)
        corpus = body.get("corpus", None)
        task_data = {
            "texts": corpus
        }
        Task = QueueRequestTask(data=task_data, task_type_label="core_sent")

        #
        await Task.to_worker()

        #
        worker_response = await Task.get_content()
        time = 0
        while worker_response is None and time < 1800:
            worker_response = await Task.get_content()
            time += 1
            await asyncio.sleep(0.1)
        else:
            # return self.write_json({
            #     'get parameter': task_data,
            #     "worker response": json.loads(worker_response)
            # })
            if worker_response is not None:
                result = json.loads(worker_response)["content"]
                return self.write_json(result)
            else:
                return self.write_json({
                    "status": "worker time-out",
                    "data": str(worker_response)
                })


