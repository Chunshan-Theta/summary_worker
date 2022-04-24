import json

from handler.api.apiHandlerBase import APIHandlerBase
from util.aredis_queue import QueueRequestTask
import asyncio
from util.ArticleCutter import interface_convolution

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
                            "其實你很棒知道自己因為害怕別人的眼光而造就自己體貼的個性或許這樣的性格也是讓你更懂得應對進退至於緊張的狀況下次感受到大家的注目試著先閉上眼睛深呼吸告訴自己沒問題然後再張開眼睛開始動作也許就能緩解那種緊張心情喔"
                        ]
        responses:
            200:
              description: test
        """
        body = json.loads(self.request.body)
        inputs = body.get("corpus", None)
        corpus = []
        for input in inputs:
            corpus+=[s for s in interface_convolution(input) if len(s)>0]
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


